"""Abas do Check: Prefeitura ativa e documentos RV por referência exata."""

import pandas as pd


def build_check(
    prefeitura_df: pd.DataFrame, fs10n_df: pd.DataFrame
) -> dict[str, pd.DataFrame]:
    active = prefeitura_df[
        prefeitura_df["Nf Ativa"].astype(str).str.upper().eq("SIM")
    ].copy()
    cancelled = prefeitura_df[
        prefeitura_df["Nf Ativa"].astype(str).str.contains("CANCEL", case=False, na=False)
    ].copy()
    prefeitura_nfs = set(active["Numero NF"].astype(str).str.strip())
    references = fs10n_df["Referência"].fillna("").astype(str).str.strip()
    document_types = fs10n_df["Tipo de documento"].fillna("").astype(str).str.upper()
    issued = fs10n_df[
        document_types.eq("RV") & references.isin(prefeitura_nfs)
    ].copy()
    reversed_documents = fs10n_df[document_types.eq("EF")].copy()
    cancellations = fs10n_df[document_types.isin(["EF", "DG"])].copy()
    sap_references = set(issued["Referência"].astype(str).str.strip())
    exceptions = active[
        active["Numero NF"].astype(str).str.strip().isin(prefeitura_nfs - sap_references)
    ].copy()
    exceptions["Status Conciliação"] = "Não Conciliada"
    exceptions["Motivo"] = "Pendente Classificação"
    prefeitura_balance = active["Valor Serviço"].sum()
    # Absoluto da soma dos RV encontrados; não é a soma dos absolutos da FS10N.
    sap_balance = abs(issued["Montante em moeda interna"].astype(float).sum())
    summary = pd.DataFrame({
        "Indicador": [
            "Saldo Prefeitura", "Saldo SAP", "Diferença", "Qtd Exceções", "Valor Exceções"
        ],
        "Valor": [
            prefeitura_balance, sap_balance, prefeitura_balance - sap_balance,
            len(exceptions), exceptions["Valor Serviço"].sum(),
        ],
    })
    return {
        "SAP x Prefeitura": summary,
        "Prefeitura Emitidas": active,
        "Notas Emitidas Razao": issued,
        "Estornadas Razao": reversed_documents,
        "Prefeitura Canceladas": cancelled,
        "Cancelamentos": cancellations,
        "Excecoes": exceptions,
    }
