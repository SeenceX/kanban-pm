from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str #= "db" # localhost для IDE, db - для DOCKER
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@db:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file="./backend/.env")


settings = Settings()