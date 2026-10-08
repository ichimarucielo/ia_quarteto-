from src.ingestion.prefeitura_reader import (
    PrefeituraReader,
)

from src.ingestion.fs10n_reader import (
    FS10NReader,
)

from src.services.data_normalization_service import (
    DataNormalizationService,
)

from src.services.check_workbook_service import (
    CheckWorkbookService,
)


def print_section(
    title: str,
) -> None:

    print(
        f"\n===== {title} =====\n"
    )


def main() -> None:

    prefeitura_df = (
        PrefeituraReader().read()
    )

    prefeitura_df = (
        DataNormalizationService
        .normalize_prefeitura(
            prefeitura_df
        )
    )

    fs10n_df = (
        FS10NReader().read()
    )

    workbook = (
        CheckWorkbookService.build(
            prefeitura_df=prefeitura_df,
            fs10n_df=fs10n_df,
        )
    )

    print_section(
        "CHECK WORKBOOK PROFILE"
    )

    print_section(
        "SAP x PREFEITURA"
    )

    print(
        workbook.sap_x_prefeitura
        .to_string(index=False)
    )

    print_section(
        "PREFEITURA - NOTAS EMITIDAS"
    )

    print(
        f"Linhas.............: "
        f"{len(workbook.prefeitura_notas_emitidas):,}"
    )

    print(
        f"NFs................: "
        f"{workbook.prefeitura_notas_emitidas['Numero NF'].nunique():,}"
    )

    print(
        f"Valor..............: "
        f"{workbook.prefeitura_notas_emitidas['Valor Serviço'].sum():,.2f}"
    )

    print_section(
        "NOTAS EMITIDAS - RAZÃO"
    )

    notas_emitidas_razao = (
        workbook.notas_emitidas_razao
    )

    print(
        f"Linhas.............: "
        f"{len(notas_emitidas_razao):,}"
    )

    print(
        f"Saldo..............: "
        f"{abs(
            notas_emitidas_razao[
                'Montante em moeda interna'
            ]
            .astype(float)
            .sum()
        ):,.2f}"
    )

    print_section(
        "ESTORNADAS - RAZÃO"
    )

    estornadas_razao = (
        workbook.estornadas_razao
    )

    print(
        f"Linhas.............: "
        f"{len(estornadas_razao):,}"
    )

    print(
        f"Saldo..............: "
        f"{abs(
            estornadas_razao[
                'Montante em moeda interna'
            ]
            .astype(float)
            .sum()
        ):,.2f}"
    )

    print_section(
        "PREFEITURA - CANCELADAS"
    )

    canceladas = (
        workbook.prefeitura_canceladas
    )

    print(
        f"Linhas.............: "
        f"{len(canceladas):,}"
    )

    print(
        f"Valor..............: "
        f"{canceladas['Valor Serviço'].sum():,.2f}"
    )

    print_section(
        "CANCELAMENTOS"
    )

    print(
        f"Linhas.............: "
        f"{len(workbook.cancelamentos):,}"
    )

    print_section(
        "TOP CANCELADAS"
    )

    print(
        canceladas[
            [
                "Numero NF",
                "Tomador",
                "Valor Serviço",
            ]
        ]
        .sort_values(
            by="Valor Serviço",
            ascending=False,
        )
        .head(20)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()