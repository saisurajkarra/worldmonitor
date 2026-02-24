from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_env: str = 'development'
    log_level: str = 'INFO'
    lmop_csv_path: str
    wwtp_csv_path: str
    cattle_csv_path: str
    news_api_url: str
    news_api_key: str
    competitor_pdf_dir: str
    request_timeout_s: float = 20.0
    breaker_fail_max: int = 4
    breaker_reset_timeout_s: int = 60


settings = Settings()
