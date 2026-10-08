import pandas as pd


class ZSD008PrefeituraAnalysis:

    @staticmethod
    def execute(
        prefeitura_df: pd.DataFrame,
        zsd008_df: pd.DataFrame,
    ) -> None:

        prefeitura_nfs = set(
            prefeitura_df["Numero NF"]
            .astype(str)
            .str.strip()
        )

        zsd_nfs = set(
            zsd008_df["Nº Nota Fiscal"]
            .astype(str)
            .str.replace(
                ".0",
                "",
                regex=False,
            )
            .str.strip()
        )

        comuns = (
            prefeitura_nfs
            & zsd_nfs
        )

        somente_prefeitura = (
            prefeitura_nfs
            - zsd_nfs
        )

        somente_zsd008 = (
            zsd_nfs
            - prefeitura_nfs
        )

        print("\n" + "=" * 80)
        print("ZSD008 x PREFEITURA")
        print("=" * 80)

        print(
            f"Prefeitura.........: {len(prefeitura_nfs):,}"
        )

        print(
            f"ZSD008.............: {len(zsd_nfs):,}"
        )

        print(
            f"Comuns.............: {len(comuns):,}"
        )

        print(
            f"Somente Prefeitura.: {len(somente_prefeitura):,}"
        )

        print(
            f"Somente ZSD008.....: {len(somente_zsd008):,}"
        )

        print("\nPrimeiras 20 somente Prefeitura")

        print(
            sorted(
                list(
                    somente_prefeitura
                )
            )[:20]
        )

        print("\n===== SOMENTE PREFEITURA =====\n")

        somente_prefeitura_df = (
            prefeitura_df[
                prefeitura_df[
                    "Numero NF"
                ]
                .astype(str)
                .isin(
                    somente_prefeitura
                )
            ]
            .copy()
        )

        cols = [
            "Numero NF",
            "Tomador",
            "Valor Serviço",
            "Nf Ativa",
        ]

        print(
            somente_prefeitura_df[
                cols
            ]
            .sort_values(
                by="Numero NF"
            )
            .to_string(
                index=False
            )
        )

        print("\nPrimeiras 20 somente ZSD008")

        print(
            sorted(
                [
                    str(x)
                    for x in somente_zsd008
                    if pd.notna(x)
                ]
            )[:20]
        )

        print("\n===== RESUMO STATUS =====\n")

        print(
            somente_prefeitura_df[
                "Nf Ativa"
            ]
            .value_counts(
                dropna=False
            )
        )

        ativos = (
            somente_prefeitura_df[
                somente_prefeitura_df[
                    "Nf Ativa"
                ]
                .astype(str)
                .eq("Sim")
            ]
            .copy()
        )

        print("\n===== ATIVOS SEM MATCH =====\n")

        if ativos.empty:

            print(
                "Nenhum documento ativo sem match."
            )

        else:

            print(
                ativos[
                    [
                        "Numero NF",
                        "Tomador",
                        "Valor Serviço",
                    ]
                ]
                .sort_values(
                    by="Numero NF"
                )
                .to_string(
                    index=False
                )
            )

        print("\n" + "=" * 80)