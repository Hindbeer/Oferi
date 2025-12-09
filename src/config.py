from pydantic_settings import BaseSettings, SettingsConfigDict

# load_dotenv()

# BOT_TOKEN: str = os.getenv("BOT_TOKEN")
# ADMIN_ID: int = os.getenv("ADMIN_ID")
# TELEGRAM_CHANNEL_ID: str = os.getenv("TELEGRAM_CHANNEL_ID")
# BOT_LINK: str = os.getenv("BOT_LINK")


class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_ID: int
    TELEGRAM_CHANNEL_ID: str
    BOT_LINK: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
