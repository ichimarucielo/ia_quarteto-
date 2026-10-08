import pandas as pd


class FS10NBusinessFilterService:
    """
    Regras de negócio específicas do FS10N.
    """

    @staticmethod
    def get_revenue_documents(
        fs10n_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Retorna apenas documentos de faturamento (RV).
        """

        filtered_df = fs10n_df[
            fs10n_df["Tipo de documento"]
            .astype(str)
            .str.strip()
            == "RV"
        ].copy()

        return filtered_df

    @staticmethod
    def get_adjustment_documents(
        fs10n_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Retorna apenas documentos de ajuste/estorno (EF).
        """

        filtered_df = fs10n_df[
            fs10n_df["Tipo de documento"]
            .astype(str)
            .str.strip()
            == "EF"
        ].copy()

        return filtered_df

    @staticmethod
    def summarize_document_types(
        fs10n_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Retorna resumo dos tipos documentais.
        """

        summary_df = (
            fs10n_df["Tipo de documento"]
            .astype(str)
            .str.strip()
            .value_counts()
            .reset_index()
        )

        summary_df.columns = [
            "TipoDocumento",
            "Quantidade"
        ]

        return summary_df