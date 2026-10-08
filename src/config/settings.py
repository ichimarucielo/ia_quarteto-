from pathlib import Path


class Settings:
    """
    Configurações globais da aplicação.
    Centraliza paths e constantes do projeto.
    """

    PROJECT_ROOT = Path(__file__).resolve().parents[2]

    DATA_PATH = PROJECT_ROOT / "data"

    RAW_PATH = DATA_PATH / "raw"
    PROCESSED_PATH = DATA_PATH / "processed"
    OUTPUT_PATH = DATA_PATH / "output"

    LOG_PATH = PROJECT_ROOT / "logs"

    FS10N_PATH = RAW_PATH / "fs10n"
    PREFEITURA_PATH = RAW_PATH / "prefeitura"
    ZSD008_PATH = RAW_PATH / "zsd008"


settings = Settings()