import pandas as pd


class DataNormalizationService:
    """
    Responsável por normalizar datasets antes
    da execução das regras de negócio.
    """

    @staticmethod
    def normalize_fs10n(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df = df.copy()

        df.columns = [
            str(col).strip()
            for col in df.columns
        ]

        empty_columns = [
            col
            for col in df.columns
            if col.lower() == "nan"
        ]

        if empty_columns:
            df.drop(
                columns=empty_columns,
                inplace=True,
                errors="ignore",
            )

        df["Montante em moeda interna"] = pd.to_numeric(
            df["Montante em moeda interna"],
            errors="coerce",
        ).fillna(0)

        return df

    @staticmethod
    def normalize_prefeitura(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df = df.copy()

        df.columns = [
            str(col).strip()
            for col in df.columns
        ]

        monetary_columns = [
            "Valor Serviço",
            "Total NF",
            "Valor Fatura",
        ]

        for column in monetary_columns:

            if column not in df.columns:
                continue

            df[column] = (
                df[column]
                .astype(str)
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
            )

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce",
            ).fillna(0)

        if "CNPJ" in df.columns:

            df["CNPJ"] = (
                df["CNPJ"]
                .astype(str)
                .str.replace(".0", "", regex=False)
                .str.strip()
                .str.zfill(14)
            )

        key_columns = [
            "Numero NF",
            "Numerp RPS",
            "NF Substituida por",
        ]

        for column in key_columns:

            if column not in df.columns:
                continue

            df[column] = (
                df[column]
                .astype(str)
                .str.replace(".0", "", regex=False)
                .str.strip()
            )

        if "Chave de acesso da NFS-e" in df.columns:

            df["Chave de acesso da NFS-e"] = (
                df["Chave de acesso da NFS-e"]
                .astype(str)
                .str.replace(".0", "", regex=False)
                .str.strip()
            )

        return df