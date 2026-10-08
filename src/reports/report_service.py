import pandas as pd


class ReportService:

    @staticmethod
    def build(
        zsd008_df: pd.DataFrame,
    ) -> pd.DataFrame:

        report_df = (
            zsd008_df.copy()
        )

        report_df = (
            report_df[
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
                    "Substituição",
                ]
            ]
            .copy()
        )

        report_df.sort_values(
            by=[
                "Nº Nota Fiscal",
                "Descrição",
            ],
            inplace=True,
        )

        report_df.reset_index(
            drop=True,
            inplace=True,
        )

        return report_df