from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    hostname: str
    password: str
    db_name: str
    username: str
    db_port: str

    # jwt settings
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = '.env'

settings = Settings()