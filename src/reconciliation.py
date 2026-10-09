"""Cruzamento de existência por NF usado na aba Nao_Conciliadas.

Uma NF presente nas duas fontes fica fora desta aba, mesmo se houver diferença
de valor ou cancelamento. Mudar esses critérios exige uma mudança de regra.
"""

import pandas as pd

from src.normalization import normalize_nf


def find_unmatched(
    prefeitura_df: pd.DataFrame, billing_df: pd.DataFrame
) -> pd.DataFrame:
    prefeitura, billing = prefeitura_df.copy(), billing_df.copy()
    prefeitura["_nf"] = normalize_nf(prefeitura["Numero NF"])
    billing["_nf"] = normalize_nf(billing["Nº Nota Fiscal"])
    invalid_keys = {"", "nan", "none", "0"}
    prefeitura = prefeitura[~prefeitura["_nf"].isin(invalid_keys)]
    billing = billing[~billing["_nf"].isin(invalid_keys)]
    prefeitura_by_nf = prefeitura.groupby("_nf", as_index=False).agg({
        "Numero NF": "first", "Tomador": "first",
        "Valor Serviço": "sum", "Nf Ativa": "first",
    }).set_index("_nf", drop=False)
    billing_by_nf = billing.groupby("_nf", as_index=False).agg({
        "Nº Nota Fiscal": "first", "Razão Social": "first", "Valor Bruto": "sum",
    }).set_index("_nf", drop=False)
    prefeitura_keys = set(prefeitura_by_nf["_nf"])
    billing_keys = set(billing_by_nf["_nf"])
    rows = []
    for nf in sorted(prefeitura_keys - billing_keys):
        row = prefeitura_by_nf.loc[nf]
        rows.append({
            "Status Conciliação": "Não Conciliada",
            "Tipo Exceção": "PREFEITURA_SEM_BILLING",
            "NF Prefeitura": row["Numero NF"], "NF Billing": "",
            "Cliente Prefeitura": row["Tomador"], "Cliente Billing": "",
            "Valor Prefeitura": row["Valor Serviço"], "Valor Billing": 0,
            "Diferença": row["Valor Serviço"],
            "Motivo": "NF emitida na Prefeitura sem correspondência no Billing",
            "Status NF Prefeitura": row["Nf Ativa"],
        })
    for nf in sorted(billing_keys - prefeitura_keys):
        row = billing_by_nf.loc[nf]
        rows.append({
            "Status Conciliação": "Não Conciliada",
            "Tipo Exceção": "BILLING_SEM_PREFEITURA",
            "NF Prefeitura": "", "NF Billing": row["Nº Nota Fiscal"],
            "Cliente Prefeitura": "", "Cliente Billing": row["Razão Social"],
            "Valor Prefeitura": 0, "Valor Billing": row["Valor Bruto"],
            "Diferença": -row["Valor Bruto"],
            "Motivo": "NF existente no Billing sem correspondência na Prefeitura",
            "Status NF Prefeitura": "",
        })
    return pd.DataFrame(rows, columns=[
        "Status Conciliação", "Tipo Exceção", "NF Prefeitura", "NF Billing",
        "Cliente Prefeitura", "Cliente Billing", "Valor Prefeitura", "Valor Billing",
        "Diferença", "Motivo", "Status NF Prefeitura",
    ])
