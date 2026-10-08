import pandas as pd


class SchemaValidator:
    """
    Responsável por validar os layouts dos arquivos.
    """

    PREFEITURA_REQUIRED_COLUMNS = [
        "Numero NF",
        "CNPJ",
        "Tomador",
        "Valor Serviço",
        "Total NF",
        "Nf Ativa",
    ]

    FS10N_REQUIRED_COLUMNS = [
        "Conta",
        "Nº documento",
        "Texto",
        "Tipo de documento",
        "Montante em moeda interna",
    ]

    @staticmethod
    def validate_prefeitura(df: pd.DataFrame) -> None:

        missing_columns = [
            column
            for column in SchemaValidator.PREFEITURA_REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing_columns:

            raise ValueError(
                "Colunas obrigatórias ausentes na Prefeitura: "
                f"{missing_columns}"
            )

    @staticmethod
    def validate_fs10n(df: pd.DataFrame) -> None:

        missing_columns = [
            column
            for column in SchemaValidator.FS10N_REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing_columns:

            raise ValueError(
                "Colunas obrigatórias ausentes no FS10N: "
                f"{missing_columns}"
            )