import pandas as pd


class BillingMatchingService:

    @staticmethod
    def execute(
        prefeitura_df: pd.DataFrame,
        zsd008_df: pd.DataFrame,
    ) -> pd.DataFrame:

        prefeitura = prefeitura_df.copy()

        zsd008 = zsd008_df.copy()

        prefeitura["Numero NF"] = (
            prefeitura["Numero NF"]
            .astype(str)
            .str.strip()
        )

        zsd008["Nº Nota Fiscal"] = (
            zsd008["Nº Nota Fiscal"]
            .astype(str)
            .str.replace(
                ".0",
                "",
                regex=False,
            )
            .str.strip()
        )

        notas_emitidas_df = (
            zsd008.merge(
                prefeitura[
                    [
                        "Numero NF",
                        "Nf Ativa",
                    ]
                ],
                left_on="Nº Nota Fiscal",
                right_on="Numero NF",
                how="inner",
            )
        )

        return (
            notas_emitidas_df[
                [
                    "Razão Social",
                    "CNPJ",
                    "Descrição",
                    "Nº Nota Fiscal",
                    "N° RPS",
                    "Fatura Billing",
                    "Data RPS",
                    "Valor Bruto",
                    "Período",
                    "Data Vencimento",
                    "Discriminação",
                    "Link  NFS-e",
                    "Link  Boleto",
                    "Qtde Transação",
                    "Preço Unitário",
                    "Empresa",
                    "Nf Ativa",
                ]
            ]
            .copy()
        )