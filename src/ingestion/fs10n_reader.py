from pathlib import Path

import pandas as pd

from src.utils.logger import get_logger


logger = get_logger(__name__)


class FS10NReader:

    def __init__(
        self,
        file_path: Path
    ) -> None:

        self.file_path = Path(file_path)

    def read(self) -> pd.DataFrame:

        logger.info(
            f"Lendo arquivo FS10N: "
            f"{self.file_path.name}"
        )

        raw_df = pd.read_excel(
            self.file_path,
            header=None,
            engine="openpyxl",
        )

        header_row = raw_df.iloc[0].tolist()

        df = raw_df.iloc[1:].copy()

        df.columns = header_row

        df.reset_index(
            drop=True,
            inplace=True,
        )

        logger.info(
            f"Arquivo FS10N carregado. "
            f"Registros: {len(df):,}"
        )

        return df