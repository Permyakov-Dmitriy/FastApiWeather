from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    LIST_MAJOR_CITIES: list[str] = ['moscow', 'london', 'tokyo', 'new york', 'beijing']
    TOKEN: str
    URL_API_WEATHER: str


    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()