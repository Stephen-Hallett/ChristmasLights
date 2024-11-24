from pydantic_settings import BaseSettings  #


class Settings(BaseSettings):
    app_name: str = "ChristmasLights"
    cors_allow_origins: list = ["*"]

    debug: bool = False


settings = Settings()