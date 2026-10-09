"""Leitura das três fontes, sem regras de conciliação ou escrita de arquivos."""

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def read_prefeitura(file_path: Path) -> pd.DataFrame:
    # Identificadores são texto: zeros à esquerda fazem parte do dado original.
    identifiers = {
        column: str
        for column in (
            "CNPJ", "Numero NF", "Numerp RPS", "NF Substituida por",
            "Chave de acesso da NFS-e", "Código de Autenticidade",
        )
    }
    logger.info("Lendo Prefeitura: %s", file_path)
    last_error = None
    for encoding in ("utf-8", "latin1", "cp1252"):
        try:
            dataframe = pd.read_csv(
                file_path, sep=";", encoding=encoding,
                dtype=identifiers, low_memory=False,
            )
            logger.info("Prefeitura: %s linhas (%s)", len(dataframe), encoding)
            return dataframe
        except UnicodeDecodeError as error:
            last_error = error
    raise ValueError(f"Não foi possível ler Prefeitura: {file_path}") from last_error


def read_fs10n(file_path: Path) -> pd.DataFrame:
    logger.info("Lendo FS10N: %s", file_path)
    # Preserva a leitura original: cabeçalho separado, sem inferir tipos por coluna.
    raw = pd.read_excel(file_path, header=None, engine="openpyxl")
    dataframe = raw.iloc[1:].copy()
    dataframe.columns = raw.iloc[0].tolist()
    dataframe.reset_index(drop=True, inplace=True)
    logger.info("FS10N: %s linhas", len(dataframe))
    return dataframe


def read_zsd008(file_path: Path) -> pd.DataFrame:
    logger.info("Lendo ZSD008: %s", file_path)
    dataframe = pd.read_excel(file_path, engine="openpyxl")
    logger.info("ZSD008: %s linhas", len(dataframe))
    return dataframe
