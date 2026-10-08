from src.ingestion.prefeitura_reader import (
    PrefeituraReader,
)

from src.ingestion.zsd008_reader import (
    ZSD008Reader,
)

from src.services.data_normalization_service import (
    DataNormalizationService,
)

from src.reports.report_service import (
    ReportService,
)

from src.services.report_workbook_service import (
    ReportWorkbookService,
)


def print_section(
    title: str,
) -> None:

    print(
        f"\n===== {title} =====\n"
    )


def main() -> None:

    prefeitura_df = (
        PrefeituraReader().read()
    )

    prefeitura_df = (
        DataNormalizationService
        .normalize_prefeitura(
            prefeitura_df
        )
    )

    zsd008_df = (
        ZSD008Reader().read()
    )

    report_df = (
        ReportService.build(
            zsd008_df=zsd008_df,
        )
    )

    workbook = (
        ReportWorkbookService.build(
            report_df=report_df,
            prefeitura_df=prefeitura_df,
        )
    )

    print_section(
        "REPORT WORKBOOK PROFILE"
    )

    print_section(
        "SAP x PREFEITURA"
    )

    print(
        workbook.sap_x_prefeitura
        .to_string(index=False)
    )

    print_section(
        "NOTAS EMITIDAS"
    )

    print(
        f"Linhas.............: "
        f"{len(workbook.notas_emitidas):,}"
    )

    print(
        f"NFs................: "
        f"{workbook.notas_emitidas['Nº Nota Fiscal'].nunique():,}"
    )

    print(
        f"Valor..............: "
        f"{workbook.notas_emitidas['Valor Bruto'].sum():,.2f}"
    )

    print_section(
        "SETUP"
    )

    print(
        f"Linhas.............: "
        f"{len(workbook.setup):,}"
    )

    print(
        f"NFs................: "
        f"{workbook.setup['Nº Nota Fiscal'].nunique():,}"
    )

    print(
        f"Valor..............: "
        f"{workbook.setup['Valor Bruto'].sum():,.2f}"
    )

    print(
        "\n===== TOP SETUP =====\n"
    )

    print(
        workbook.setup[
            [
                "Razão Social",
                "Nº Nota Fiscal",
                "Valor Bruto",
            ]
        ]
        .sort_values(
            by="Valor Bruto",
            ascending=False,
        )
        .head(20)
        .to_string(index=False)
    )

    print_section(
        "CONTRATOS CIELO"
    )

    print(
        f"Linhas.............: "
        f"{len(workbook.contratos_cielo):,}"
    )

    print(
        f"NFs................: "
        f"{workbook.contratos_cielo['Nº Nota Fiscal'].nunique():,}"
    )

    print(
        f"Valor..............: "
        f"{workbook.contratos_cielo['Valor Bruto'].sum():,.2f}"
    )

    print(
        "\n===== TOP CONTRATOS CIELO =====\n"
    )

    print(
        workbook.contratos_cielo[
            [
                "Razão Social",
                "Descrição",
                "Nº Nota Fiscal",
                "Fatura Billing",
                "Valor Bruto",
            ]
        ]
        .sort_values(
            by="Valor Bruto",
            ascending=False,
        )
        .head(50)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()