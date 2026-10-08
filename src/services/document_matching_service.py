import pandas as pd

from src.services.document_exceptions_service import (
    ReferenceNormalizationService
)


class DocumentMatchingService:
    """
    Responsável por identificar documentos conciliados
    e documentos ausentes entre Prefeitura e SAP.
    """

    @staticmethod
    def execute(
        prefeitura_df: pd.DataFrame,
        fs10n_rv_df: pd.DataFrame,
    ) -> dict:

        prefeitura_nfs = (
            prefeitura_df["Numero NF"]
            .astype(str)
            .str.strip()
        )

        sap_refs = (
            fs10n_rv_df["Referência"]
            .apply(
                ReferenceNormalizationService.normalize
            )
            .dropna()
            .astype(str)
            .str.strip()
        )

        sap_refs = sap_refs[
            sap_refs != "0"
        ]

        sap_refs = sap_refs[
            sap_refs != ""
        ]

        prefeitura_set = set(prefeitura_nfs)

        sap_set = set(sap_refs)

        matched = prefeitura_set & sap_set

        only_prefeitura = prefeitura_set - sap_set

        only_sap = sap_set - prefeitura_set

        return {
            "matched": matched,
            "only_prefeitura": only_prefeitura,
            "only_sap": only_sap,
        }