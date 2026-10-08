import pandas as pd


class CancellationMatchingV2Service:

    TOLERANCE = 0.01

    @staticmethod
    def execute(
        prefeitura_df: pd.DataFrame,
        fs10n_ef_df: pd.DataFrame,
    ) -> pd.DataFrame:

        prefeitura_canceladas = prefeitura_df[
            prefeitura_df["Nf Ativa"]
            .astype(str)
            .str.upper()
            .eq("CANCELADA")
        ].copy()

        results = []

        used_ef_indexes = set()

        for _, nf_row in prefeitura_canceladas.iterrows():

            numero_nf = str(
                nf_row["Numero NF"]
            ).strip()

            numero_rps = str(
                nf_row["Numerp RPS"]
            ).strip()

            cliente = (
                str(nf_row["Tomador"])
                .upper()
                .strip()
            )

            valor_nf = round(
                float(
                    nf_row["Valor Serviço"]
                ),
                2,
            )

            #
            # PRIORIDADE 1
            # RPS explícito
            #
            matching_efs = fs10n_ef_df[
                fs10n_ef_df["Referência"]
                .astype(str)
                .str.contains(
                    numero_rps,
                    na=False,
                )
            ]

            metodo_match = "RPS"

            #
            # PRIORIDADE 2
            # NF explícita
            #
            if matching_efs.empty:

                matching_efs = fs10n_ef_df[
                    fs10n_ef_df["Referência"]
                    .astype(str)
                    .str.contains(
                        numero_nf,
                        na=False,
                    )
                ]

                metodo_match = "NF"

            #
            # PRIORIDADE 3
            # Cliente
            #
            if matching_efs.empty:

                matching_efs = fs10n_ef_df[
                    fs10n_ef_df["Texto"]
                    .astype(str)
                    .str.upper()
                    .str.contains(
                        cliente[:15],
                        na=False,
                    )
                ]

                metodo_match = "CLIENTE"

            matching_efs = matching_efs[
                ~matching_efs.index.isin(
                    used_ef_indexes
                )
            ]

            valor_ef = round(
                matching_efs[
                    "Montante em moeda interna"
                ].sum(),
                2,
            )

            diferenca = round(
                valor_nf - valor_ef,
                2,
            )

            status = (
                "CONCILIADO"
                if abs(diferenca)
                <= CancellationMatchingV2Service.TOLERANCE
                else "DIVERGENTE"
            )

            if status == "CONCILIADO":

                used_ef_indexes.update(
                    matching_efs.index
                )

            results.append(
                {
                    "NumeroNF": numero_nf,
                    "NumeroRPS": numero_rps,
                    "Cliente": cliente,
                    "ValorNF": valor_nf,
                    "ValorEF": valor_ef,
                    "Diferenca": diferenca,
                    "QtdEF": len(matching_efs),
                    "MetodoMatch": metodo_match,
                    "Status": status,
                    "Confidence": (
                        "ALTA"
                        if metodo_match in [
                            "RPS",
                            "NF",
                        ]
                        else "MEDIA"
                    ),
                }
            )

        result_df = pd.DataFrame(results)

        return result_df.sort_values(
            by="Diferenca",
            key=lambda x: x.abs(),
        )