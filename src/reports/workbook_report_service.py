from pathlib import Path

import pandas as pd

from src.config.settings import settings


class WorkbookReportService:
    """
    Responsável por gerar o workbook final
    do fechamento de faturamento.
    """

    @staticmethod
    def export(
        executive_df: pd.DataFrame,
        exceptions_df: pd.DataFrame,
        classification_result: dict,
        cancellation_v2_df: pd.DataFrame,
        file_name: str = "fechamento_faturamento.xlsx",
    ) -> Path:

        settings.OUTPUT_PATH.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_file = (
            settings.OUTPUT_PATH
            / file_name
        )

        if output_file.exists():

            try:
                output_file.unlink()

            except PermissionError:

                raise PermissionError(
                    f"O arquivo '{output_file.name}' "
                    "está aberto. Feche o Excel."
                )

        conciliacao_rv_df = pd.DataFrame(
            {
                "Documento": sorted(
                    list(
                        classification_result[
                            "conciliado_rv"
                        ]
                    )
                )
            }
        )

        cancelamentos_conciliados_df = (
            cancellation_v2_df[
                cancellation_v2_df["Status"]
                == "CONCILIADO"
            ]
        )

        cancelamentos_divergentes_df = (
            cancellation_v2_df[
                cancellation_v2_df["Status"]
                == "DIVERGENTE"
            ]
        )

        with pd.ExcelWriter(
            output_file,
            engine="openpyxl",
        ) as writer:

            executive_df.to_excel(
                writer,
                sheet_name="Resumo_Executivo",
                index=False,
            )

            exceptions_df.to_excel(
                writer,
                sheet_name="Excecoes",
                index=False,
            )

            conciliacao_rv_df.to_excel(
                writer,
                sheet_name="Conciliacao_RV",
                index=False,
            )

            cancelamentos_conciliados_df.to_excel(
                writer,
                sheet_name="Cancelamentos_Conciliados",
                index=False,
            )

            cancelamentos_divergentes_df.to_excel(
                writer,
                sheet_name="Cancelamentos_Divergentes",
                index=False,
            )

        return output_file