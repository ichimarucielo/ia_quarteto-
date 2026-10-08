from src.ingestion.prefeitura_reader import (
    PrefeituraReader,
)

from src.ingestion.fs10n_reader import (
    FS10NReader,
)

from src.services.data_normalization_service import (
    DataNormalizationService,
)

from src.reports.check_service import (
    CheckService,
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

    check_df = (
        CheckService.build(
            prefeitura_df=prefeitura_df,
            fs10n_df=fs10n_df,
        )
    )

    print("\n===== CHECK =====\n")

    print(
        f"Linhas.............: "
        f"{len(check_df):,}"
    )

    print(
        f"NFs................: "
        f"{check_df['Numero NF'].nunique():,}"
    )

    print(
        f"Valor..............: "
        f"{check_df['Valor Serviço'].sum():,.2f}"
    )

    print("\n===== HEAD =====\n")

    print(
        check_df
        .head(20)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()