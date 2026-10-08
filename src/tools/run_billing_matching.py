from src.ingestion.prefeitura_reader import (
    PrefeituraReader,
)

from src.ingestion.zsd008_reader import (
    ZSD008Reader,
)

from src.services.data_normalization_service import (
    DataNormalizationService,
)

from src.services.billing_matching_service import (
    BillingMatchingService,
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

    notas_emitidas_df = (
        BillingMatchingService.execute(
            prefeitura_df=prefeitura_df,
            zsd008_df=zsd008_df,
        )
    )

    print("\n===== NOTAS EMITIDAS =====\n")

    print(
        f"Linhas: "
        f"{len(notas_emitidas_df):,}"
    )

    print(
        f"NFs: "
        f"{notas_emitidas_df['Nº Nota Fiscal'].nunique():,}"
    )

    print(
        f"Valor Total: "
        f"{notas_emitidas_df['Valor Bruto'].sum():,.2f}"
    )

    print()

    print(
        notas_emitidas_df
        .head(20)
        .to_string(index=False)
    )

    print(
        notas_emitidas_df["Período"]
        .value_counts()
        .sort_index()
    )

if __name__ == "__main__":
    main()