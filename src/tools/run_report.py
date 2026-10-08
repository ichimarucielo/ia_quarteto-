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

    print("\n===== COLUNAS ZSD008 =====\n")

    for col in zsd008_df.columns:
        print(repr(col))

    report_df = (
        ReportService.build(
            zsd008_df=zsd008_df,
        )
    )

    print("\n===== REPORT =====\n")

    print(
        f"Linhas.............: "
        f"{len(report_df):,}"
    )

    print(
        f"NFs................: "
        f"{report_df['Nº Nota Fiscal'].nunique():,}"
    )

    print(
        f"Valor..............: "
        f"{report_df['Valor Bruto'].sum():,.2f}"
    )

    print("\n===== HEAD =====\n")

    print(
        report_df
        .head(20)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()