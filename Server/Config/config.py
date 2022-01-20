from dataclasses import dataclass


@dataclass
class Config:

    DATABASE_NAME: str = "juniverse"
    DATABASE_PORT_NUMBER: int = 3306
    DATABASE_ADDRESS: str = '127.0.0.1'
    DATABASE_USER_NAME: str = 'root'
    DATABASE_USER_PASSWORD: str = 'webtoon'

    SERVER_URL_ADDRESS: str = '0.0.0.0'
    SERVER_URL_SCHEME: str = 'http'
    SERVER_PORT_NUMBER: int = 8000


config_args = Config()




