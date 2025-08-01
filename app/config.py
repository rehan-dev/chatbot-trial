from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key: str = "smdk390dlk9(randomdk939))asdklasdkl"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    openai_key: str = ""

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings() # type: ignore