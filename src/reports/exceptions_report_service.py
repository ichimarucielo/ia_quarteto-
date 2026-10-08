import pandas as pd


class ExceptionsReportService:
    """
    Consolida apenas exceções reais encontradas
    durante o processo de conciliação.
    """

    @staticmethod
    def execute(
        divergence_result: dict,
        cancellation_v2_df: pd.DataFrame,
        prefeitura_df: pd.DataFrame,
        fs10n_df: pd.DataFrame,
    ) -> pd.DataFrame:

        exceptions = []

        cancelamentos_conciliados = set(
            cancellation_v2_df[
                cancellation_v2_df["Status"]
                == "CONCILIADO"
            ]["NumeroNF"]
            .astype(str)
        )

        #
        # Prefeitura sem SAP
        #
        for doc in divergence_result[
            "only_prefeitura_docs"
        ]:

            if str(doc) in cancelamentos_conciliados:
                continue

            match = prefeitura_df[
                prefeitura_df["Numero NF"]
                .astype(str)
                .eq(str(doc))
            ]

            if match.empty:
                continue

            row = match.iloc[0]

            exceptions.append(
                {
                    "Status": "EXCECAO",
                    "TipoExcecao":
                        "PREFEITURA_SEM_SAP",
                    "Documento": doc,
                    "Cliente": row["Tomador"],
                    "Valor": row["Valor Serviço"],
                    "Origem": "PREFEITURA",
                    "Detalhes": row["Nf Ativa"],
                }
            )

        #
        # SAP sem Prefeitura
        #
        for doc in divergence_result[
            "only_sap_docs"
        ]:

            match = fs10n_df[
                fs10n_df["Referência"]
                .astype(str)
                .str.contains(
                    str(doc),
                    na=False,
                )
            ]

            if match.empty:
                continue

            row = match.iloc[0]

            exceptions.append(
                {
                    "Status": "EXCECAO",
                    "TipoExcecao":
                        "SAP_SEM_PREFEITURA",
                    "Documento": doc,
                    "Cliente": row["Texto"],
                    "Valor": row[
                        "Montante em moeda interna"
                    ],
                    "Origem": "SAP",
                    "Detalhes": row[
                        "Tipo de documento"
                    ],
                }
            )

        #
        # Cancelamentos divergentes V2
        #
        divergentes = cancellation_v2_df[
            cancellation_v2_df["Status"]
            == "DIVERGENTE"
        ]

        for _, row in divergentes.iterrows():

            exceptions.append(
                {
                    "Status": "EXCECAO",
                    "TipoExcecao":
                        "CANCELAMENTO_DIVERGENTE",
                    "Documento":
                        row["NumeroNF"],
                    "Cliente":
                        row["Cliente"],
                    "Valor":
                        row["ValorNF"],
                    "Origem":
                        "PREFEITURA",
                    "Detalhes":
                        (
                            f"Metodo={row['MetodoMatch']}; "
                            f"Diferenca={row['Diferenca']}"
                        ),
                }
            )

        return pd.DataFrame(
            exceptions
        )