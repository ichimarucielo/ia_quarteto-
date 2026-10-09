"""Normalização existente, preservada para manter os resultados dos relatórios."""

import pandas as pd


def normalize_fs10n(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe = dataframe.copy()
    dataframe.columns = [str(column).strip() for column in dataframe.columns]
    empty_columns = [column for column in dataframe.columns if column.lower() == "nan"]
    dataframe.drop(columns=empty_columns, inplace=True, errors="ignore")
    dataframe["Montante em moeda interna"] = pd.to_numeric(
        dataframe["Montante em moeda interna"], errors="coerce"
    ).fillna(0)
    return dataframe


def normalize_prefeitura(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe = dataframe.copy()
    dataframe.columns = [str(column).strip() for column in dataframe.columns]
    for column in ("Valor Serviço", "Total NF", "Valor Fatura"):
        if column in dataframe.columns:
            values = (
                dataframe[column].astype(str)
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
            )
            dataframe[column] = pd.to_numeric(values, errors="coerce").fillna(0)
    if "CNPJ" in dataframe.columns:
        dataframe["CNPJ"] = (
            dataframe["CNPJ"].astype(str)
            .str.replace(".0", "", regex=False).str.strip().str.zfill(14)
        )
    for column in (
        "Numero NF", "Numerp RPS", "NF Substituida por", "Chave de acesso da NFS-e"
    ):
        if column in dataframe.columns:
            dataframe[column] = (
                dataframe[column].astype(str)
                .str.replace(".0", "", regex=False).str.strip()
            )
    return dataframe


def normalize_nf(series: pd.Series) -> pd.Series:
    """Chave do Report; não altera os identificadores exibidos nas abas."""
    return series.fillna("").astype(str).str.strip().str.replace(r"\.0$", "", regex=True)
