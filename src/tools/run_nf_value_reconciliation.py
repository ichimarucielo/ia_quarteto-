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

import pandas as pd


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

    prefeitura_valores = (
        prefeitura_df
        .copy()
    )

    prefeitura_valores[
        "Numero NF"
    ] = (
        prefeitura_valores[
            "Numero NF"
        ]
        .astype(str)
        .str.strip()
    )

    prefeitura_valores = (
        prefeitura_valores
        .groupby(
            "Numero NF",
            as_index=False,
        )
        .agg(
            {
                "Tomador": "first",
                "Valor Serviço": "sum",
                "Nf Ativa": "first",
            }
        )
    )

    billing_valores = (
        notas_emitidas_df
        .copy()
    )

    billing_valores[
        "Nº Nota Fiscal"
    ] = (
        billing_valores[
            "Nº Nota Fiscal"
        ]
        .astype(str)
        .str.strip()
    )

    billing_valores = (
        billing_valores
        .groupby(
            "Nº Nota Fiscal",
            as_index=False,
        )
        .agg(
            {
                "Valor Bruto": "sum",
            }
        )
    )

    reconciliation_df = (
        prefeitura_valores
        .merge(
            billing_valores,
            left_on="Numero NF",
            right_on="Nº Nota Fiscal",
            how="left",
        )
    )

    reconciliation_df[
        "Valor Bruto"
    ] = (
        reconciliation_df[
            "Valor Bruto"
        ]
        .fillna(0)
    )

    reconciliation_df[
        "Diferenca"
    ] = (
        reconciliation_df[
            "Valor Serviço"
        ]
        -
        reconciliation_df[
            "Valor Bruto"
        ]
    )

    reconciliation_df[
        "Diferenca Absoluta"
    ] = (
        reconciliation_df[
            "Diferenca"
        ]
        .abs()
    )

    top_diffs = (
        reconciliation_df
        .sort_values(
            by="Diferenca Absoluta",
            ascending=False,
        )
        .head(20)
    )

    print(
        "\n===== TOP 20 DIFERENÇAS =====\n"
    )

    print(
        top_diffs[
            [
                "Numero NF",
                "Tomador",
                "Nf Ativa",
                "Valor Serviço",
                "Valor Bruto",
                "Diferenca",
            ]
        ]
        .to_string(
            index=False
        )
    )

    print(
        "\n===== RESUMO =====\n"
    )

    print(
        f"Valor Prefeitura: "
        f"{reconciliation_df['Valor Serviço'].sum():,.2f}"
    )

    print(
        f"Valor Billing: "
        f"{reconciliation_df['Valor Bruto'].sum():,.2f}"
    )

    print(
        f"Diferença: "
        f"{reconciliation_df['Diferenca'].sum():,.2f}"
    )

    print(
        f"NFs com diferença: "
        f"{(reconciliation_df['Diferenca Absoluta'] > 0.01).sum():,}"
    )


if __name__ == "__main__":
    main()