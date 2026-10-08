from src.ingestion.zsd008_reader import (
    ZSD008Reader,
)

from src.reports.report_service import (
    ReportService,
)


def main() -> None:

    zsd008_df = (
        ZSD008Reader().read()
    )

    report_df = (
        ReportService.build(
            zsd008_df=zsd008_df,
        )
    )

    print(
        "\n===== REPORT PROFILE =====\n"
    )

    print(
        f"Linhas.............: {len(report_df):,}"
    )

    print(
        f"NFs................: "
        f"{report_df['Nº Nota Fiscal'].nunique():,}"
    )

    print(
        f"Valor..............: "
        f"{report_df['Valor Bruto'].sum():,.2f}"
    )

    print(
        "\n===== DESCRIÇÃO - QTD =====\n"
    )

    print(
        report_df["Descrição"]
        .value_counts()
        .to_string()
    )

    print(
        "\n===== DESCRIÇÃO - VALOR =====\n"
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

    print(
        "\n===== TOP CLIENTES =====\n"
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
        .head(30)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()