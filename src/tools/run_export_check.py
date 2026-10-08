from pathlib import Path

from src.ingestion.prefeitura_reader import (
    PrefeituraReader,
)

from src.ingestion.fs10n_reader import (
    FS10NReader,
)

from src.services.data_normalization_service import (
    DataNormalizationService,
)

from src.services.check_workbook_service import (
    CheckWorkbookService,
)

from src.exporters.check_excel_exporter import (
    CheckExcelExporter,
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

    fs10n_df = (
        FS10NReader().read()
    )

    workbook = (
        CheckWorkbookService.build(
            prefeitura_df=prefeitura_df,
            fs10n_df=fs10n_df,
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
        CheckExcelExporter.export(
            workbook=workbook,
            output_dir=output_dir,
        )
    )

    print(
        f"\nArquivo gerado: {output_path}\n"
    )


if __name__ == "__main__":
    main()