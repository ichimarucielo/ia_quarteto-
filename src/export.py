"""Único ponto de escrita Excel; recebe abas prontas, sem cálculos de negócio."""

from pathlib import Path
from typing import Mapping

import pandas as pd


def export_workbook(sheets: Mapping[str, pd.DataFrame], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for name, dataframe in sheets.items():
            dataframe.to_excel(writer, sheet_name=name, index=False)
    return output_path
