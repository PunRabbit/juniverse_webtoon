import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv(verbose=True)


@dataclass
class Config:

    DATABASE_NAME: str = os.getenv('database_name')
    DATABASE_PORT_NUMBER: int = int(os.getenv('database_port_number'))
    DATABASE_ADDRESS: str = os.getenv('database_address')
    DATABASE_ROOT_USER_NAME: str = os.getenv('database_root_user_name')
    DATABASE_ROOT_USER_PASSWORD: str = os.getenv('database_root_user_password')

    SERVER_URL_ADDRESS: str = os.getenv('server_url_address')
    SERVER_URL_SCHEME: str = os.getenv('server_url_scheme')
    SERVER_PORT_NUMBER: int = int(os.getenv('server_port_number'))


config_args = Config()




