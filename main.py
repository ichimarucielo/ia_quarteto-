"""CLI único para gerar ou inspecionar os relatórios de conciliação."""

import argparse
import logging
from pathlib import Path

import pandas as pd

from src.check import build_check
from src.export import export_workbook
from src.ingestion import read_fs10n, read_prefeitura, read_zsd008
from src.normalization import normalize_fs10n, normalize_prefeitura
from src.report import build_report

PROJECT_ROOT = Path(__file__).resolve().parent
logger = logging.getLogger(__name__)


def build_workbooks(
    prefeitura_file: Path, fs10n_file: Path, zsd008_file: Path
) -> dict[str, dict[str, pd.DataFrame]]:
    prefeitura = normalize_prefeitura(read_prefeitura(prefeitura_file))
    fs10n = normalize_fs10n(read_fs10n(fs10n_file))
    billing = read_zsd008(zsd008_file)
    return {
        "Check_Faturamento.xlsx": build_check(prefeitura, fs10n),
        "Report_Faturamento.xlsx": build_report(prefeitura, billing),
    }


def print_analysis(workbooks: dict[str, dict[str, pd.DataFrame]]) -> None:
    """Diagnóstico das mesmas abas, sem exportar ou aplicar regras adicionais."""
    for filename, sheets in workbooks.items():
        print(f"\n{filename}")
        print(sheets["SAP x Prefeitura"].to_string(index=False))
        print("\nLinhas por aba:")
        for name, dataframe in sheets.items():
            print(f"  {name}: {len(dataframe)}")
    unmatched = workbooks["Report_Faturamento.xlsx"]["Nao_Conciliadas"]
    print("\nAusências por origem:")
    print(unmatched.groupby("Tipo Exceção", sort=False).agg(
        NFs=("Tipo Exceção", "size"), Diferenca=("Diferença", "sum")
    ).to_string())
    print("\n20 maiores ausências por valor absoluto:")
    top = unmatched.loc[
        unmatched["Diferença"].abs().sort_values(ascending=False).head(20).index
    ]
    print(top.to_string(index=False))
    billing = workbooks["Report_Faturamento.xlsx"]["Notas Emitidas"]
    for column in ("Razão Social", "Descrição", "Período", "Fatura Billing"):
        print(f"\nBilling por {column} (até 20 grupos):")
        print(billing.groupby(column)["Valor Bruto"].sum()
              .sort_values(ascending=False).head(20).to_string())


def get_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Conciliação fiscal Prefeitura/SAP/Billing")
    for source in ("prefeitura", "fs10n", "zsd008"):
        parser.add_argument(f"--{source}", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=PROJECT_ROOT / "data/output")
    parser.add_argument("--analisar", action="store_true",
                        help="Mostra resumos e ausências sem gerar arquivos.")
    args = parser.parse_args(argv)
    for source in ("prefeitura", "fs10n", "zsd008"):
        path = getattr(args, source)
        if not path.is_file():
            parser.error(f"Arquivo de {source} não encontrado: {path}")
    return args


def configure_logging(analyze: bool) -> None:
    handlers = [logging.StreamHandler()]
    if not analyze:
        log_dir = PROJECT_ROOT / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_dir / "reconciliation.log", encoding="utf-8"))
    logging.basicConfig(
        level=logging.INFO, handlers=handlers, force=True,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def main(argv: list[str] | None = None) -> list[Path]:
    args = get_arguments(argv)
    configure_logging(args.analisar)
    logger.info("Iniciando processamento")
    workbooks = build_workbooks(args.prefeitura, args.fs10n, args.zsd008)
    if args.analisar:
        print_analysis(workbooks)
        return []
    outputs = []
    for filename, sheets in workbooks.items():
        output = export_workbook(sheets, args.output_dir / filename)
        outputs.append(output)
        logger.info("Arquivo gerado: %s", output)
    logger.info("Processamento concluído")
    return outputs


if __name__ == "__main__":
    main()
