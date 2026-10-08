from dataclasses import dataclass

import pandas as pd


@dataclass(slots=True)
class CheckWorkbook:

    sap_x_prefeitura: pd.DataFrame

    prefeitura_notas_emitidas: pd.DataFrame

    notas_emitidas_razao: pd.DataFrame

    estornadas_razao: pd.DataFrame

    prefeitura_canceladas: pd.DataFrame

    cancelamentos: pd.DataFrame

    excecoes: pd.DataFrame


class CheckWorkbookService:

    @staticmethod
    def build(
        prefeitura_df: pd.DataFrame,
        fs10n_df: pd.DataFrame,
    ) -> CheckWorkbook:

        prefeitura_notas_emitidas = (
            prefeitura_df[
                prefeitura_df["Nf Ativa"]
                .astype(str)
                .str.upper()
                .eq("SIM")
            ]
            .copy()
        )

        prefeitura_canceladas = (
            prefeitura_df[
                prefeitura_df["Nf Ativa"]
                .astype(str)
                .str.contains(
                    "CANCEL",
                    case=False,
                    na=False,
                )
            ]
            .copy()
        )

        prefeitura_nfs = set(
            prefeitura_notas_emitidas[
                "Numero NF"
            ]
            .astype(str)
            .str.strip()
        )

        referencia_str = (
            fs10n_df["Referência"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        tipo_documento = (
            fs10n_df["Tipo de documento"]
            .fillna("")
            .astype(str)
            .str.upper()
        )

        notas_emitidas_razao = (
            fs10n_df[
                tipo_documento.eq("RV")
                &
                referencia_str.isin(
                    prefeitura_nfs
                )
            ]
            .copy()
        )

        estornadas_razao = (
            fs10n_df[
                tipo_documento.eq("EF")
            ]
            .copy()
        )

        cancelamentos = (
            fs10n_df[
                tipo_documento.isin(
                    [
                        "EF",
                        "DG",
                    ]
                )
            ]
            .copy()
        )

        referencias_sap = set(
            notas_emitidas_razao[
                "Referência"
            ]
            .astype(str)
            .str.strip()
        )

        nfs_excecao = (
            prefeitura_nfs
            - referencias_sap
        )

        excecoes = (
            prefeitura_notas_emitidas[
                prefeitura_notas_emitidas[
                    "Numero NF"
                ]
                .astype(str)
                .str.strip()
                .isin(
                    nfs_excecao
                )
            ]
            .copy()
        )

        excecoes[
            "Status Conciliação"
        ] = (
            "Não Conciliada"
        )

        excecoes[
            "Motivo"
        ] = (
            "Pendente Classificação"
        )

        saldo_prefeitura = (
            prefeitura_notas_emitidas[
                "Valor Serviço"
            ]
            .sum()
        )

        saldo_sap = abs(
            notas_emitidas_razao[
                "Montante em moeda interna"
            ]
            .astype(float)
            .sum()
        )

        valor_excecoes = (
            excecoes[
                "Valor Serviço"
            ]
            .sum()
        )

        sap_x_prefeitura = (
            pd.DataFrame(
                {
                    "Indicador": [
                        "Saldo Prefeitura",
                        "Saldo SAP",
                        "Diferença",
                        "Qtd Exceções",
                        "Valor Exceções",
                    ],
                    "Valor": [
                        saldo_prefeitura,
                        saldo_sap,
                        saldo_prefeitura
                        - saldo_sap,
                        len(excecoes),
                        valor_excecoes,
                    ],
                }
            )
        )

        return CheckWorkbook(
            sap_x_prefeitura=sap_x_prefeitura,
            prefeitura_notas_emitidas=prefeitura_notas_emitidas,
            notas_emitidas_razao=notas_emitidas_razao,
            estornadas_razao=estornadas_razao,
            prefeitura_canceladas=prefeitura_canceladas,
            cancelamentos=cancelamentos,
            excecoes=excecoes,
        )