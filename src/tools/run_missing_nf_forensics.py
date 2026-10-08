from src.ingestion.prefeitura_reader import PrefeituraReader
from src.ingestion.zsd008_reader import ZSD008Reader

from src.services.data_normalization_service import (
    DataNormalizationService,
)

from src.services.billing_matching_service import (
    BillingMatchingService,
)

import pandas as pd


def main() -> None:

    prefeitura_df = PrefeituraReader().read()

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

    matched_nfs = {
        str(nf).strip()
        for nf in notas_emitidas_df[
            "Nº Nota Fiscal"
        ]
        .dropna()
        .unique()
    }

    prefeitura_df = (
        prefeitura_df.copy()
    )

    prefeitura_df[
        "Numero NF"
    ] = (
        prefeitura_df[
            "Numero NF"
        ]
        .astype(str)
        .str.strip()
    )

    missing_df = (
        prefeitura_df[
            ~prefeitura_df[
                "Numero NF"
            ]
            .isin(
                matched_nfs
            )
        ]
        .copy()
    )

    missing_nfs = (
        missing_df[
            "Numero NF"
        ]
        .drop_duplicates()
        .tolist()
    )

    print(
        "\n===== NFS SEM MATCH =====\n"
    )

    print(
        f"Total: {len(missing_nfs)}"
    )

    zsd = (
        zsd008_df.copy()
    )

    zsd[
        "NF_STR"
    ] = (
        zsd[
            "Nº Nota Fiscal"
        ]
        .astype(str)
        .str.strip()
    )

    zsd[
        "SUBSTITUICAO_STR"
    ] = (
        zsd[
            "Substituição"
        ]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    results = []

    for nf in missing_nfs:

        prefeitura_row = (
            missing_df[
                missing_df[
                    "Numero NF"
                ]
                == nf
            ]
            .iloc[0]
        )

        direct_match = (
            zsd[
                zsd[
                    "NF_STR"
                ]
                == nf
            ]
        )

        substitution_match = (
            zsd[
                zsd[
                    "SUBSTITUICAO_STR"
                ]
                == nf
            ]
        )

        results.append(
            {
                "NF":
                    nf,

                "Status":
                    prefeitura_row[
                        "Nf Ativa"
                    ],

                "Tomador":
                    prefeitura_row[
                        "Tomador"
                    ],

                "Valor Serviço":
                    prefeitura_row[
                        "Valor Serviço"
                    ],

                "Existe na ZSD008":
                    not direct_match.empty,

                "Qtd Registros":
                    len(
                        direct_match
                    ),

                "Encontrada Como Substituida":
                    not substitution_match.empty,

                "Qtd Substituicoes":
                    len(
                        substitution_match
                    ),
            }
        )

    result_df = (
        pd.DataFrame(
            results
        )
        .sort_values(
            by="Valor Serviço",
            ascending=False,
        )
    )

    print(
        result_df.to_string(
            index=False
        )
    )

    print(
        "\n===== SOMENTE ATIVAS =====\n"
    )

    print(
        result_df[
            result_df[
                "Status"
            ]
            == "Sim"
        ]
        .to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()