from src.ingestion.prefeitura_reader import PrefeituraReader
from src.ingestion.zsd008_reader import ZSD008Reader

from src.services.data_normalization_service import (
    DataNormalizationService,
)


def main() -> None:

    prefeitura_df = PrefeituraReader().read()

    prefeitura_df = (
        DataNormalizationService
        .normalize_prefeitura(prefeitura_df)
    )

    zsd_df = ZSD008Reader().read()

    prefeitura_nfs = set(
        prefeitura_df["Numero NF"]
        .astype(str)
        .str.strip()
    )

    zsd_nfs = set(
        zsd_df["Nº Nota Fiscal"]
        .astype(str)
        .str.strip()
    )

    matched_nfs = (
        prefeitura_nfs & zsd_nfs
    )

    missing_nfs = (
        prefeitura_nfs - zsd_nfs
    )

    matched_df = prefeitura_df[
        prefeitura_df["Numero NF"]
        .astype(str)
        .str.strip()
        .isin(matched_nfs)
    ]

    missing_df = prefeitura_df[
        prefeitura_df["Numero NF"]
        .astype(str)
        .str.strip()
        .isin(missing_nfs)
    ]

    print("\n===== REPORT VALIDATION =====\n")

    print(
        f"Total NFs Prefeitura......: {len(prefeitura_nfs):,}"
    )

    print(
        f"Total NFs Billing.........: {len(zsd_nfs):,}"
    )

    print(
        f"NFs Match................: {len(matched_nfs):,}"
    )

    print(
        f"NFs Sem Match............: {len(missing_nfs):,}"
    )

    coverage = (
        len(matched_nfs)
        / len(prefeitura_nfs)
        * 100
    )

    print(
        f"Cobertura................: {coverage:.2f}%"
    )

    print(
        f"Valor Match..............: "
        f"{matched_df['Valor Serviço'].sum():,.2f}"
    )

    print(
        f"Valor Sem Match..........: "
        f"{missing_df['Valor Serviço'].sum():,.2f}"
    )

    print("\n===== TOP EXCEÇÕES =====\n")

    print(
        missing_df[
            [
                "Numero NF",
                "Tomador",
                "Valor Serviço",
                "Nf Ativa",
            ]
        ]
        .sort_values(
            "Valor Serviço",
            ascending=False,
        )
        .head(20)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()