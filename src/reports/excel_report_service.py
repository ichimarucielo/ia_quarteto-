from pathlib import Path

import pandas as pd

from src.config.settings import settings


class ExcelReportService:
    """
    Responsável pela geração de relatórios Excel.
    """

    @staticmethod
    def export(
        dataframe: pd.DataFrame,
        file_name: str,
    ) -> Path:

        settings.OUTPUT_PATH.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_file = (
            settings.OUTPUT_PATH
            / file_name
        )

        with pd.ExcelWriter(
            output_file,
            engine="openpyxl",
        ) as writer:

            dataframe.to_excel(
                writer,
                sheet_name="Dados",
                index=False,
            )

            worksheet = writer.sheets["Dados"]

            for column in worksheet.columns:

                max_length = 0

                column_letter = (
                    column[0].column_letter
                )

                for cell in column:

                    try:

                        max_length = max(
                            max_length,
                            len(str(cell.value))
                        )

                    except Exception:
                        pass

                worksheet.column_dimensions[
                    column_letter
                ].width = min(
                    max_length + 2,
                    60
                )

        return output_file