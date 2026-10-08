from src.ingestion.prefeitura_reader import (
    PrefeituraReader,
)

from src.ingestion.zsd008_reader import (
    ZSD008Reader,
)

from src.services.data_normalization_service import (
    DataNormalizationService,
)

from src.reports.report_service import (
    ReportService,
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

    zsd008_df = (
        ZSD008Reader().read()
    )

    report_df = (
        ReportService.build(
            zsd008_df=zsd008_df,
        )
    )

    print_section(
        "CONTRACTS PROFILE"
    )

    print(
        f"Linhas.............: "
        f"{len(report_df):,}"
    )

    print(
        f"NFs................: "
        f"{report_df['Nº Nota Fiscal'].nunique():,}"
    )

    print(
        f"Clientes...........: "
        f"{report_df['Razão Social'].nunique():,}"
    )

    print(
        f"Valor..............: "
        f"{report_df['Valor Bruto'].sum():,.2f}"
    )

    print_section(
        "TOP CLIENTES"
    )

    print(
        report_df.groupby(
            "Razão Social",
            as_index=False,
        )["Valor Bruto"]
        .sum()
        .sort_values(
            "Valor Bruto",
            ascending=False,
        )
        .head(50)
        .to_string(index=False)
    )

    print_section(
        "TOP PRODUTOS"
    )

    print(
        report_df.groupby(
            "Descrição",
            as_index=False,
        )["Valor Bruto"]
        .sum()
        .sort_values(
            "Valor Bruto",
            ascending=False,
        )
        .to_string(index=False)
    )

    print_section(
        "TOP FATURAS BILLING"
    )

    print(
        report_df.groupby(
            "Fatura Billing",
            as_index=False,
        )["Valor Bruto"]
        .sum()
        .sort_values(
            "Valor Bruto",
            ascending=False,
        )
        .head(50)
        .to_string(index=False)
    )

    print_section(
        "CLIENTE x PRODUTO"
    )

    print(
        report_df.groupby(
            [
                "Razão Social",
                "Descrição",
            ],
            as_index=False,
        )["Valor Bruto"]
        .sum()
        .sort_values(
            "Valor Bruto",
            ascending=False,
        )
        .head(100)
        .to_string(index=False)
    )

    print_section(
        "CLIENTE x FATURA"
    )

    print(
        report_df.groupby(
            [
                "Razão Social",
                "Fatura Billing",
            ],
            as_index=False,
        )["Valor Bruto"]
        .sum()
        .sort_values(
            "Valor Bruto",
            ascending=False,
        )
        .head(100)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()