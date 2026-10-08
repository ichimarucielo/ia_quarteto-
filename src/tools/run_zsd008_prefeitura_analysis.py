from src.analysis.zsd008_prefeitura_analysis import (
    ZSD008PrefeituraAnalysis,
)

from src.ingestion.prefeitura_reader import (
    PrefeituraReader,
)

from src.ingestion.zsd008_reader import (
    ZSD008Reader,
)

from src.services.data_normalization_service import (
    DataNormalizationService,
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

    ZSD008PrefeituraAnalysis.execute(
        prefeitura_df=prefeitura_df,
        zsd008_df=zsd008_df,
    )


if __name__ == "__main__":
    main()