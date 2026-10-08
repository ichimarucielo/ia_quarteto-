class CancellationRules:

    CANCELLED_STATUS = "CANCELADA"

    SAP_CANCELLATION_TYPES = {
        "EF"
    }

    MINIMUM_MATCH_FIELDS = [
        "cliente",
        "valor"
    ]