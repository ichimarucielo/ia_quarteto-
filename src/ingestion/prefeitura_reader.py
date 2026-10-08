from pathlib import Path

import pandas as pd

from src.utils.logger import get_logger


logger = get_logger(__name__)


class PrefeituraReader:

    STRING_COLUMNS = {
        "CNPJ": str,
        "Numero NF": str,
        "Numerp RPS": str,
        "NF Substituida por": str,
        "Chave de acesso da NFS-e": str,
        "Código de Autenticidade": str,
    }

    def __init__(
        self,
        file_path: Path
    ) -> None:

        self.file_path = Path(file_path)

    def read(self) -> pd.DataFrame:

        logger.info(
            f"Lendo arquivo prefeitura: "
            f"{self.file_path.name}"
        )

        encodings = [
            "utf-8",
            "latin1",
            "cp1252",
        ]

        last_error = None

        for encoding in encodings:

            try:

                df = pd.read_csv(
                    self.file_path,
                    sep=";",
                    encoding=encoding,
                    dtype=self.STRING_COLUMNS,
                    low_memory=False,
                )

                logger.info(
                    f"Arquivo prefeitura carregado. "
                    f"Encoding: {encoding}. "
                    f"Registros: {len(df):,}"
                )

                return df

            except UnicodeDecodeError as error:

                last_error = error

        raise RuntimeError(
            f"Não foi possível ler "
            f"{self.file_path.name}"
        ) from last_error