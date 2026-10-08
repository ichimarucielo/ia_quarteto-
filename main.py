import argparse
from pathlib import Path

from src.config.settings import settings

from src.ingestion.prefeitura_reader import (
    PrefeituraReader,
)

from src.ingestion.fs10n_reader import (
    FS10NReader,
)

from src.ingestion.zsd008_reader import (
    ZSD008Reader,
)

from src.services.data_normalization_service import (
    DataNormalizationService,
)

from src.services.check_workbook_service import (
    CheckWorkbookService,
)

from src.services.report_workbook_service import (
    ReportWorkbookService,
)

from src.reports.report_service import (
    ReportService,
)

from src.exporters.check_excel_exporter import (
    CheckExcelExporter,
)

from src.exporters.report_excel_exporter import (
    ReportExcelExporter,
)

from src.utils.logger import (
    get_logger,
)


logger = get_logger(__name__)


def run_check(
    prefeitura_file: Path,
    fs10n_file: Path,
) -> None:

    logger.info(
        "Gerando CHECK"
    )

    prefeitura_df = (
        PrefeituraReader(
            prefeitura_file
        ).read()
    )

    prefeitura_df = (
        DataNormalizationService
        .normalize_prefeitura(
            prefeitura_df
        )
    )

    fs10n_df = (
        FS10NReader(
            fs10n_file
        ).read()
    )

    fs10n_df = (
        DataNormalizationService
        .normalize_fs10n(
            fs10n_df
        )
    )

    workbook = (
        CheckWorkbookService.build(
            prefeitura_df=prefeitura_df,
            fs10n_df=fs10n_df,
        )
    )

    output_path = (
        CheckExcelExporter.export(
            workbook=workbook,
            output_dir=settings.OUTPUT_PATH,
        )
    )

    logger.info(
        f"Check gerado: {output_path}"
    )


def run_report(
    prefeitura_file: Path,
    zsd008_file: Path,
) -> None:

    logger.info(
        "Gerando REPORT"
    )

    prefeitura_df = (
        PrefeituraReader(
            prefeitura_file
        ).read()
    )

    prefeitura_df = (
        DataNormalizationService
        .normalize_prefeitura(
            prefeitura_df
        )
    )

    zsd008_df = (
        ZSD008Reader(
            zsd008_file
        ).read()
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

    output_path = (
        ReportExcelExporter.export(
            workbook=workbook,
            output_dir=settings.OUTPUT_PATH,
        )
    )

    logger.info(
        f"Report gerado: {output_path}"
    )


def get_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--prefeitura",
        required=True
    )

    parser.add_argument(
        "--fs10n",
        required=True
    )

    parser.add_argument(
        "--zsd008",
        required=True
    )

    return parser.parse_args()


def main() -> None:

    args = get_arguments()

    prefeitura_file = Path(
        args.prefeitura
    )

    fs10n_file = Path(
        args.fs10n
    )

    zsd008_file = Path(
        args.zsd008
    )

    logger.info(
        "Iniciando processamento"
    )

    settings.OUTPUT_PATH.mkdir(
        parents=True,
        exist_ok=True,
    )

    run_check(
        prefeitura_file=prefeitura_file,
        fs10n_file=fs10n_file,
    )

    run_report(
        prefeitura_file=prefeitura_file,
        zsd008_file=zsd008_file,
    )

    logger.info(
        "Processamento concluído"
    )


if __name__ == "__main__":
    main()