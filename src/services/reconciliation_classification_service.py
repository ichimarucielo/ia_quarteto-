import pandas as pd


class ReconciliationClassificationService:
    """
    Classifica os resultados da conciliação.
    """

    @staticmethod
    def execute(
        match_result: dict,
        cancellation_v2_df: pd.DataFrame,
    ) -> dict:

        conciliados_cancelamento = (
            cancellation_v2_df[
                cancellation_v2_df["Status"]
                == "CONCILIADO"
            ]
            .to_dict("records")
        )

        divergentes_cancelamento = (
            cancellation_v2_df[
                cancellation_v2_df["Status"]
                == "DIVERGENTE"
            ]
            .to_dict("records")
        )

        return {
            "conciliado_rv":
                match_result["matched"],

            "excecao_prefeitura":
                match_result["only_prefeitura"],

            "excecao_sap":
                match_result["only_sap"],

            "conciliado_cancelamento":
                conciliados_cancelamento,

            "excecao_cancelamento":
                divergentes_cancelamento,
        }