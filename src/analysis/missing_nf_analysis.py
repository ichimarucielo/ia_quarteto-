import pandas as pd


class MissingNFAnalysis:

    @staticmethod
    def execute(
        prefeitura_df: pd.DataFrame,
        zsd008_df: pd.DataFrame,
    ) -> None:

        prefeitura_nfs = set(
            prefeitura_df["Numero NF"]
            .astype(str)
            .str.strip()
        )

        zsd_nfs = set(
            zsd008_df["Nº Nota Fiscal"]
            .astype(str)
            .str.replace(
                ".0",
                "",
                regex=False,
            )
            .str.strip()
        )

        missing_nfs = (
            prefeitura_nfs
            - zsd_nfs
        )

        missing_df = prefeitura_df[
            prefeitura_df["Numero NF"]
            .astype(str)
            .isin(missing_nfs)
        ].copy()

        print(
            "\n===== MISSING NFS =====\n"
        )

        print(
            missing_df[
                [
                    "Numero NF",
                    "Tomador",
                    "Valor Serviço",
                    "Nf Ativa",
                ]
            ]
            .sort_values(
                by="Numero NF"
            )
            .to_string(
                index=False
            )
        )

        print(
            "\n===== RESUMO =====\n"
        )

        print(
            missing_df[
                "Nf Ativa"
            ].value_counts()
        )

        print(
            "\nValor Total Faltante:"
        )

        print(
            round(
                missing_df[
                    "Valor Serviço"
                ].sum(),
                2,
            )
        )