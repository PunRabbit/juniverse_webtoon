import bcrypt
from bcrypt import hashpw, gensalt
from abc import abstractmethod, ABCMeta, ABC
from Server.Config.config import config_args


class BcryptModel(metaclass=ABCMeta):

    @abstractmethod
    async def bcrypt_key(self) -> str:
        pass

    @abstractmethod
    async def bcrypt_password(self, password: str) -> str:
        pass

    @abstractmethod
    async def bcrypt_word(self, word: str) -> str:
        pass

    @abstractmethod
    async def bcrypt_number(self, number: str) -> str:
        pass

    @abstractmethod
    async def check_bcrypt(self, input_type: str) -> bool:
        pass


class BcryptLevel1(BcryptModel, ABC):

    # 현재 따로 속성값을 조회하는 경우는 없으나 일단 Default 값으로 작성한 상태
    def __init__(self):
        self.key: str = config_args.SERVER_BCRYPT_KEY

    @classmethod
    async def bcrypt_key(cls) -> str:
        byte_key: bytes = config_args.SERVER_BCRYPT_KEY.encode('UTF-8')
        bcrypt_key: str = hashpw(byte_key, gensalt(12)).decode('UTF-8')
        return bcrypt_key

    @classmethod
    async def bcrypt_password(cls, password: str) -> str:
        byte_password: bytes = password.encode('UTF-8')
        bcrypt_password: str = hashpw(byte_password, gensalt(12)).decode('UTF-8')
        return bcrypt_password

    @classmethod
    async def bcrypt_word(cls, word: str) -> str:
        byte_word: bytes = word.encode('UTF-8')
        bcrypt_word: str = hashpw(byte_word, gensalt(12)).decode('UTF-8')
        return bcrypt_word

    @classmethod
    async def bcrypt_number(cls, number: str) -> str:
        byte_number: bytes = number.encode('UTF-8')
        bcrypt_word: str = hashpw(byte_number, gensalt(12)).decode('UTF-8')
        return bcrypt_word

    @classmethod
    async def check_bcrypt(cls, input_str: str) -> bool:
        database_key = "12"  # database class가 아직 없으므로 임시 더미 작성
        if bcrypt.checkpw(database_key.encode('UTF-8'), config_args.SERVER_BCRYPT_KEY):
            pass