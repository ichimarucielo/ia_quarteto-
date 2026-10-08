from pathlib import Path

import pandas as pd

from src.utils.logger import get_logger


logger = get_logger(__name__)


class ZSD008Reader:

    def __init__(
        self,
        file_path: Path
    ) -> None:

        self.file_path = Path(file_path)

    def read(self) -> pd.DataFrame:

        logger.info(
            f"Lendo arquivo ZSD008: "
            f"{self.file_path.name}"
        )

        df = pd.read_excel(
            self.file_path,
            engine="openpyxl",
        )

        logger.info(
            f"Arquivo ZSD008 carregado. "
            f"Registros: {len(df):,}"
        )

        return df