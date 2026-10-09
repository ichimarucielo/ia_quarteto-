"""Abas do Report: Billing completo, resumo e ausências por NF."""

import pandas as pd

from src.reconciliation import find_unmatched

BILLING_COLUMNS = [
    "Razão Social", "CNPJ", "Descrição", "Nº Nota Fiscal", "N° RPS", "Fatura Billing",
    "Data RPS", "Valor Bruto", "Período", "Data Vencimento", "Discriminação",
    "Link  NFS-e", "Link  Boleto", "Qtde Transação", "Preço Unitário", "Substituição",
]


def build_report(
    prefeitura_df: pd.DataFrame, zsd008_df: pd.DataFrame
) -> dict[str, pd.DataFrame]:
    billing = zsd008_df[BILLING_COLUMNS].copy()
    billing.sort_values(by=["Nº Nota Fiscal", "Descrição"], inplace=True)
    billing.reset_index(drop=True, inplace=True)
    setup = billing[
        billing["Descrição"].astype(str).str.contains("SETUP", case=False, na=False)
    ].copy()
    contracts = billing[
        billing["Razão Social"].astype(str).str.contains("CIELO", case=False, na=False)
    ].copy()
    prefeitura_balance = prefeitura_df["Valor Serviço"].sum()
    billing_balance = billing["Valor Bruto"].sum()
    summary = pd.DataFrame({
        "Indicador": [
            "Saldo Prefeitura", "Saldo Billing", "Diferença",
            "Qtd NFs Prefeitura", "Qtd NFs Billing",
        ],
        "Valor": [
            prefeitura_balance, billing_balance, prefeitura_balance - billing_balance,
            prefeitura_df["Numero NF"].nunique(), billing["Nº Nota Fiscal"].nunique(),
        ],
    })
    return {
        "SAP x Prefeitura": summary,
        "Notas Emitidas": billing.copy(),
        "Nao_Conciliadas": find_unmatched(prefeitura_df, billing),
        "Setup": setup,
        "Contratos Cielo": contracts,
    }
