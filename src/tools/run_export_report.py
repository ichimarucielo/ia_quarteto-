from pathlib import Path

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

from src.exporters.report_excel_exporter import (
    ReportExcelExporter,
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

    output_dir = Path(
        "data/output"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        ReportExcelExporter.export(
            workbook=workbook,
            output_dir=output_dir,
        )
    )

    print(
        f"\nArquivo gerado: {output_path}\n"
    )


if __name__ == "__main__":
    main()