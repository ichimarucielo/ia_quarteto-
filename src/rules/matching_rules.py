class MatchingRules:

    DOCUMENT_KEY_PREFEITURA = "Numero NF"

    DOCUMENT_KEY_SAP = "Referência"

    IGNORE_REFERENCES = {
        "0",
        "",
        None,
    }

    MATCH_PRIORITY = [
        "NF_EXPLICITA",
        "NF_REFERENCIA",
        "CLIENTE_VALOR",
        "VALOR"
    ]