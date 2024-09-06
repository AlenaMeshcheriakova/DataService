from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    MODE: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DECODE_RESPONSES: bool

    GRPC_HOST: str
    GRPC_PORT: int

    GRPC_AUTH_HOST: str
    GRPC_AUTH_PORT: int

    MQ_HOST: str

    @property
    def get_DB_HOST(self)-> str:
        return self.DB_HOST

    @property
    def get_DB_PORT(self) -> str:
        return str(self.DB_PORT)

    @property
    def get_DB_USER(self) -> str:
        return self.DB_USER

    @property
    def get_DB_PASS(self) -> str:
        return self.DB_PASS

    @property
    def get_DB_NAME(self) -> str:
        return self.DB_NAME

    @property
    def DATABASE_URL_asyncpg(self)-> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_psycopg(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def get_MQ_HOST(self) -> str:
        return self.MQ_HOST

    @property
    def get_REDIS_HOST(self)-> str:
        return self.REDIS_HOST

    @property
    def get_REDIS_PORT(self) -> int:
        return self.REDIS_PORT

    @property
    def get_REDIS_DECODE_RESPONSES(self) -> bool:
        return self.REDIS_DECODE_RESPONSES

    @property
    def get_AUTH_GRPC_conn(self) -> str:
        return f"{self.GRPC_AUTH_HOST}:{str(self.GRPC_AUTH_PORT)}"

    model_config = SettingsConfigDict(env_file="cfg/development/.env")

load_dotenv()
settings = Settings()