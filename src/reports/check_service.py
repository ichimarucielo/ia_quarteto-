import pandas as pd


class CheckService:

    @staticmethod
    def build(
        prefeitura_df: pd.DataFrame,
        fs10n_df: pd.DataFrame,
    ) -> pd.DataFrame:

        prefeitura = (
            prefeitura_df.copy()
        )

        fs10n = (
            fs10n_df.copy()
        )

        prefeitura[
            "Numero NF"
        ] = (
            prefeitura[
                "Numero NF"
            ]
            .astype(str)
            .str.strip()
        )

        fs10n[
            "REFERENCIA_STR"
        ] = (
            fs10n[
                "Referência"
            ]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        check_df = (
            prefeitura.merge(
                fs10n[
                    [
                        "Referência",
                        "Tipo de documento",
                        "Nº documento",
                        "Montante em moeda interna",
                        "Texto",
                        "Empresa",
                    ]
                ],
                left_on="Numero NF",
                right_on="Referência",
                how="left",
            )
        )

        check_df.sort_values(
            by=[
                "Numero NF",
            ],
            inplace=True,
        )

        check_df.reset_index(
            drop=True,
            inplace=True,
        )

        return check_df