from dataclasses import dataclass

import pandas as pd


@dataclass(slots=True)
class ReportWorkbook:

    sap_x_prefeitura: pd.DataFrame

    notas_emitidas: pd.DataFrame

    nao_conciliadas: pd.DataFrame

    setup: pd.DataFrame

    contratos_cielo: pd.DataFrame


class ReportWorkbookService:

    @staticmethod
    def _normalize_nf(series: pd.Series) -> pd.Series:
        return (
            series
            .fillna("")
            .astype(str)
            .str.strip()
            .str.replace(r"\.0$", "", regex=True)
        )

    @staticmethod
    def _build_nao_conciliadas(
        report_df: pd.DataFrame,
        prefeitura_df: pd.DataFrame,
    ) -> pd.DataFrame:
        prefeitura = prefeitura_df.copy()
        billing = report_df.copy()

        prefeitura["_nf"] = (
            ReportWorkbookService._normalize_nf(
                prefeitura["Numero NF"]
            )
        )
        billing["_nf"] = (
            ReportWorkbookService._normalize_nf(
                billing["Nº Nota Fiscal"]
            )
        )

        invalid_keys = {"", "nan", "none", "0"}
        prefeitura = prefeitura[
            ~prefeitura["_nf"].isin(invalid_keys)
        ]
        billing = billing[
            ~billing["_nf"].isin(invalid_keys)
        ]

        prefeitura_by_nf = (
            prefeitura.groupby("_nf", as_index=False)
            .agg(
                {
                    "Numero NF": "first",
                    "Tomador": "first",
                    "Valor Serviço": "sum",
                    "Nf Ativa": "first",
                }
            )
        )
        billing_by_nf = (
            billing.groupby("_nf", as_index=False)
            .agg(
                {
                    "Nº Nota Fiscal": "first",
                    "Razão Social": "first",
                    "Valor Bruto": "sum",
                }
            )
        )

        prefeitura_keys = set(prefeitura_by_nf["_nf"])
        billing_keys = set(billing_by_nf["_nf"])
        rows = []

        for nf in sorted(prefeitura_keys - billing_keys):
            row = prefeitura_by_nf.loc[
                prefeitura_by_nf["_nf"].eq(nf)
            ].iloc[0]
            rows.append(
                {
                    "Status Conciliação": "Não Conciliada",
                    "Tipo Exceção": "PREFEITURA_SEM_BILLING",
                    "NF Prefeitura": row["Numero NF"],
                    "NF Billing": "",
                    "Cliente Prefeitura": row["Tomador"],
                    "Cliente Billing": "",
                    "Valor Prefeitura": row["Valor Serviço"],
                    "Valor Billing": 0,
                    "Diferença": row["Valor Serviço"],
                    "Motivo": "NF emitida na Prefeitura sem correspondência no Billing",
                    "Status NF Prefeitura": row["Nf Ativa"],
                }
            )

        for nf in sorted(billing_keys - prefeitura_keys):
            row = billing_by_nf.loc[
                billing_by_nf["_nf"].eq(nf)
            ].iloc[0]
            rows.append(
                {
                    "Status Conciliação": "Não Conciliada",
                    "Tipo Exceção": "BILLING_SEM_PREFEITURA",
                    "NF Prefeitura": "",
                    "NF Billing": row["Nº Nota Fiscal"],
                    "Cliente Prefeitura": "",
                    "Cliente Billing": row["Razão Social"],
                    "Valor Prefeitura": 0,
                    "Valor Billing": row["Valor Bruto"],
                    "Diferença": -row["Valor Bruto"],
                    "Motivo": "NF existente no Billing sem correspondência na Prefeitura",
                    "Status NF Prefeitura": "",
                }
            )

        columns = [
            "Status Conciliação",
            "Tipo Exceção",
            "NF Prefeitura",
            "NF Billing",
            "Cliente Prefeitura",
            "Cliente Billing",
            "Valor Prefeitura",
            "Valor Billing",
            "Diferença",
            "Motivo",
            "Status NF Prefeitura",
        ]

        return pd.DataFrame(rows, columns=columns)

    @staticmethod
    def build(
        report_df: pd.DataFrame,
        prefeitura_df: pd.DataFrame,
    ) -> ReportWorkbook:

        notas_emitidas = (
            report_df.copy()
        )

        setup = (
            report_df[
                report_df["Descrição"]
                .astype(str)
                .str.contains(
                    "SETUP",
                    case=False,
                    na=False,
                )
            ]
            .copy()
        )

        contratos_cielo = (
            report_df[
                report_df["Razão Social"]
                .astype(str)
                .str.contains(
                    "CIELO",
                    case=False,
                    na=False,
                )
            ]
            .copy()
        )

        nao_conciliadas = (
            ReportWorkbookService._build_nao_conciliadas(
                report_df=report_df,
                prefeitura_df=prefeitura_df,
            )
        )

        saldo_prefeitura = (
            prefeitura_df[
                "Valor Serviço"
            ]
            .sum()
        )

        saldo_billing = (
            report_df[
                "Valor Bruto"
            ]
            .sum()
        )

        sap_x_prefeitura = (
            pd.DataFrame(
                {
                    "Indicador": [
                        "Saldo Prefeitura",
                        "Saldo Billing",
                        "Diferença",
                        "Qtd NFs Prefeitura",
                        "Qtd NFs Billing",
                    ],
                    "Valor": [
                        saldo_prefeitura,
                        saldo_billing,
                        saldo_prefeitura
                        - saldo_billing,
                        prefeitura_df[
                            "Numero NF"
                        ]
                        .nunique(),
                        report_df[
                            "Nº Nota Fiscal"
                        ]
                        .nunique(),
                    ],
                }
            )
        )

        return ReportWorkbook(
            sap_x_prefeitura=sap_x_prefeitura,
            notas_emitidas=notas_emitidas,
            nao_conciliadas=nao_conciliadas,
            setup=setup,
            contratos_cielo=contratos_cielo,
        )