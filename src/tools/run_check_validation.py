from src.ingestion.prefeitura_reader import PrefeituraReader
from src.ingestion.fs10n_reader import FS10NReader

from src.services.data_normalization_service import (
    DataNormalizationService,
)


def main() -> None:

    prefeitura_df = PrefeituraReader().read()

    prefeitura_df = (
        DataNormalizationService
        .normalize_prefeitura(prefeitura_df)
    )

    fs10n_df = FS10NReader().read()

    prefeitura_nfs = set(
        prefeitura_df["Numero NF"]
        .astype(str)
        .str.strip()
    )

    fs10n_df["REFERENCIA_STR"] = (
        fs10n_df["Referência"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    fs10n_nfs = set(
        fs10n_df["REFERENCIA_STR"]
    )

    matched_nfs = (
        prefeitura_nfs
        & fs10n_nfs
    )

    missing_nfs = (
        prefeitura_nfs
        - fs10n_nfs
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

    rv_df = fs10n_df[
        fs10n_df["Tipo de documento"]
        .astype(str)
        .str.upper()
        == "RV"
    ]

    ef_df = fs10n_df[
        fs10n_df["Tipo de documento"]
        .astype(str)
        .str.upper()
        == "EF"
    ]

    dg_df = fs10n_df[
        fs10n_df["Tipo de documento"]
        .astype(str)
        .str.upper()
        == "DG"
    ]

    st_df = fs10n_df[
        fs10n_df["Tipo de documento"]
        .astype(str)
        .str.upper()
        == "ST"
    ]

    print("\n===== CHECK VALIDATION =====\n")

    print(
        f"NFs Prefeitura..........: {len(prefeitura_nfs):,}"
    )

    print(
        f"NFs Encontradas FS10N...: {len(matched_nfs):,}"
    )

    print(
        f"NFs Não Encontradas.....: {len(missing_nfs):,}"
    )

    coverage = (
        len(matched_nfs)
        / len(prefeitura_nfs)
        * 100
    )

    print(
        f"Cobertura...............: {coverage:.2f}%"
    )

    print(
        f"Valor Encontrado........: "
        f"{matched_df['Valor Serviço'].sum():,.2f}"
    )

    print(
        f"Valor Não Encontrado....: "
        f"{missing_df['Valor Serviço'].sum():,.2f}"
    )

    print("\n===== FS10N =====\n")

    print(
        f"RV......................: {len(rv_df):,}"
    )

    print(
        f"EF......................: {len(ef_df):,}"
    )

    print(
        f"DG......................: {len(dg_df):,}"
    )

    print(
        f"ST......................: {len(st_df):,}"
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