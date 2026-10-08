from pathlib import Path

import pandas as pd

from src.services.check_workbook_service import (
    CheckWorkbook,
)


class CheckExcelExporter:

    OUTPUT_FILE = (
        "Check_Faturamento.xlsx"
    )

    @classmethod
    def export(
        cls,
        workbook: CheckWorkbook,
        output_dir: Path,
    ) -> Path:

        output_path = (
            output_dir / cls.OUTPUT_FILE
        )

        with pd.ExcelWriter(
            output_path,
            engine="openpyxl",
        ) as writer:

            workbook.sap_x_prefeitura.to_excel(
                writer,
                sheet_name="SAP x Prefeitura",
                index=False,
            )

            workbook.prefeitura_notas_emitidas.to_excel(
                writer,
                sheet_name="Prefeitura Emitidas",
                index=False,
            )

            workbook.notas_emitidas_razao.to_excel(
                writer,
                sheet_name="Notas Emitidas Razao",
                index=False,
            )

            workbook.estornadas_razao.to_excel(
                writer,
                sheet_name="Estornadas Razao",
                index=False,
            )

            workbook.prefeitura_canceladas.to_excel(
                writer,
                sheet_name="Prefeitura Canceladas",
                index=False,
            )

            workbook.cancelamentos.to_excel(
                writer,
                sheet_name="Cancelamentos",
                index=False,
            )

            workbook.excecoes.to_excel(
                writer,
                sheet_name="Excecoes",
                index=False,
            )

        return output_path