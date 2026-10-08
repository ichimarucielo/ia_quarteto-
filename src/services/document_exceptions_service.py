import re


class ReferenceNormalizationService:
    """
    Responsável por normalizar referências SAP.
    """

    @staticmethod
    def normalize(reference):
        """
        Exemplos:

        115347 -> 115347
        227801-A -> 227801
        227820 / 113402 -> 113402
        """

        if reference is None:
            return None

        reference = str(reference).strip()

        if reference == "":
            return None

        if reference.lower() == "nan":
            return None

        # Caso:
        # 227820 / 113402
        if "/" in reference:

            parts = reference.split("/")

            last_part = parts[-1].strip()

            match = re.search(r"\d+", last_part)

            if match:
                return match.group(0)

        # Caso:
        # 227801-A
        match = re.search(r"\d+", reference)

        if match:
            return match.group(0)

        return reference