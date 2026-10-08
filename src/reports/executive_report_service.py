import pandas as pd


class ExecutiveReportService:
    """
    Gera resumo executivo da conciliação.
    """

    @staticmethod
    def generate(
        prefeitura_df: pd.DataFrame,
        fs10n_df: pd.DataFrame,
        fs10n_rv_df: pd.DataFrame,
        fs10n_ef_df: pd.DataFrame,
        divergence_result: dict,
        cancellation_v2_df: pd.DataFrame,
        exceptions_df: pd.DataFrame,
    ) -> pd.DataFrame:

        sap_total = (
            fs10n_df[
                "Montante em moeda interna"
            ]
            .abs()
            .sum()
        )

        prefeitura_total = (
            prefeitura_df[
                "Valor Serviço"
            ]
            .sum()
        )

        diferenca = (
            sap_total
            - prefeitura_total
        )

        cancelamentos_conciliados = len(
            cancellation_v2_df[
                cancellation_v2_df["Status"]
                == "CONCILIADO"
            ]
        )

        cancelamentos_divergentes = len(
            cancellation_v2_df[
                cancellation_v2_df["Status"]
                == "DIVERGENTE"
            ]
        )

        report = [
            {
                "Indicador": "Valor SAP",
                "Valor": round(
                    sap_total,
                    2,
                ),
            },
            {
                "Indicador": "Valor Prefeitura",
                "Valor": round(
                    prefeitura_total,
                    2,
                ),
            },
            {
                "Indicador": "Diferença",
                "Valor": round(
                    diferenca,
                    2,
                ),
            },
            {
                "Indicador": "Documentos Conciliados",
                "Valor": divergence_result[
                    "matched_count"
                ],
            },
            {
                "Indicador": "Somente Prefeitura",
                "Valor": divergence_result[
                    "only_prefeitura_count"
                ],
            },
            {
                "Indicador": "Somente SAP",
                "Valor": divergence_result[
                    "only_sap_count"
                ],
            },
            {
                "Indicador": "Documentos RV",
                "Valor": len(
                    fs10n_rv_df
                ),
            },
            {
                "Indicador": "Documentos EF",
                "Valor": len(
                    fs10n_ef_df
                ),
            },
            {
                "Indicador": "Cancelamentos Conciliados",
                "Valor": cancelamentos_conciliados,
            },
            {
                "Indicador": "Cancelamentos Divergentes",
                "Valor": cancelamentos_divergentes,
            },
            {
                "Indicador": "Exceções Totais",
                "Valor": len(
                    exceptions_df
                ),
            },
        ]

        return pd.DataFrame(
            report
        )