from pathlib import Path

import pandas as pd

from src.services.report_workbook_service import (
    ReportWorkbook,
)


class ReportExcelExporter:

    OUTPUT_FILE = (
        "Report_Faturamento.xlsx"
    )

    @classmethod
    def export(
        cls,
        workbook: ReportWorkbook,
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

            workbook.notas_emitidas.to_excel(
                writer,
                sheet_name="Notas Emitidas",
                index=False,
            )

            workbook.nao_conciliadas.to_excel(
                writer,
                sheet_name="Nao_Conciliadas",
                index=False,
            )

            workbook.setup.to_excel(
                writer,
                sheet_name="Setup",
                index=False,
            )

            workbook.contratos_cielo.to_excel(
                writer,
                sheet_name="Contratos Cielo",
                index=False,
            )

        return output_path