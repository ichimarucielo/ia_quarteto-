# src/tools/run_july_reconciliation.py

from src.ingestion.prefeitura_reader import PrefeituraReader
from src.ingestion.zsd008_reader import ZSD008Reader

from src.services.data_normalization_service import (
    DataNormalizationService,
)

import pandas as pd


def main() -> None:

    print("\n===== CARREGANDO DADOS =====\n")

    prefeitura_df = PrefeituraReader().read()

    prefeitura_df = (
        DataNormalizationService
        .normalize_prefeitura(prefeitura_df)
    )

    zsd_df = ZSD008Reader().read()

    print("\n===== PREFEITURA =====\n")

    total_nf_prefeitura = (
        prefeitura_df["Numero NF"]
        .astype(str)
        .nunique()
    )

    total_valor_prefeitura = (
        prefeitura_df["Valor Serviço"]
        .sum()
    )

    canceladas = (
        prefeitura_df[
            prefeitura_df["Nf Ativa"]
            .astype(str)
            .str.contains(
                "Cancel",
                case=False,
                na=False,
            )
        ]
    )

    ativas = (
        prefeitura_df[
            ~prefeitura_df.index.isin(
                canceladas.index
            )
        ]
    )

    print(
        f"NFs Prefeitura........: {total_nf_prefeitura:,}"
    )

    print(
        f"Valor Prefeitura......: {total_valor_prefeitura:,.2f}"
    )

    print(
        f"Ativas................: {len(ativas):,}"
    )

    print(
        f"Canceladas............: {len(canceladas):,}"
    )

    print("\n===== ZSD008 =====\n")

    zsd_df["NF_STR"] = (
        zsd_df["Nº Nota Fiscal"]
        .astype(str)
        .str.strip()
    )

    total_nf_zsd = (
        zsd_df["NF_STR"]
        .nunique()
    )

    total_valor_zsd = (
        zsd_df["Valor Bruto"]
        .sum()
    )

    print(
        f"NFs ZSD008............: {total_nf_zsd:,}"
    )

    print(
        f"Valor ZSD008..........: {total_valor_zsd:,.2f}"
    )

    print("\n===== MATCH NF =====\n")

    prefeitura_nfs = set(
        prefeitura_df["Numero NF"]
        .astype(str)
        .str.strip()
    )

    zsd_nfs = set(
        zsd_df["NF_STR"]
        .astype(str)
        .str.strip()
    )

    matched_nfs = (
        prefeitura_nfs
        &
        zsd_nfs
    )

    missing_nfs = (
        prefeitura_nfs
        -
        zsd_nfs
    )

    print(
        f"NFs Match............: {len(matched_nfs):,}"
    )

    print(
        f"NFs Sem Match........: {len(missing_nfs):,}"
    )

    coverage = (
        len(matched_nfs)
        / len(prefeitura_nfs)
        * 100
        if prefeitura_nfs
        else 0
    )

    print(
        f"Cobertura............: {coverage:.2f}%"
    )

    missing_df = (
        prefeitura_df[
            prefeitura_df["Numero NF"]
            .astype(str)
            .isin(missing_nfs)
        ]
        .copy()
    )

    if not missing_df.empty:

        print(
            "\n===== TOP 20 NFS SEM MATCH =====\n"
        )

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

        print(
            "\nValor sem Match......: "
            f"{missing_df['Valor Serviço'].sum():,.2f}"
        )


if __name__ == "__main__":
    main()