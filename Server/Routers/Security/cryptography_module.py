import cryptography.exceptions
from cryptography.fernet import Fernet
from Server.Config.config import config_args
from Server.Database.database import DatabaseKeySaver, DatabaseKeyChecker


# 한글 암호화 미지원 (AscII 문자만 지원)
# 사이트 내에서 직접 제어하게 될 경우에 대비해서 gen_key 생성
class CryptographyKeyGenerator(DatabaseKeySaver):

    def __init__(self, key: str):
        self.server_key: str = config_args.SERVER_CRYPTOGRAPHY_KEY
        self.init_key: str = key

    async def gen_key(self) -> str:
        if self.server_key == self.init_key:
            key = Fernet.generate_key()
            await self.save_crypto_key(key.decode('UTF-8'))
            return "success"
        else:
            return "fail"


class CryptographyEncoder(DatabaseKeyChecker):
    def __init__(self):
        self.crypto_key: str = await self.check_crypto_key()

    async def encoder(self, target: str) -> bytes:
        fernet = Fernet(self.crypto_key)
        return fernet.encrypt(target.encode())


class CryptographyDecoder(DatabaseKeyChecker):

    def __init__(self):
        self.crypto_key: str = await self.check_crypto_key()

    async def decode(self, init_word: bytes) -> bool:
        if self.crypto_key == "None":
            return False
        fernet = Fernet(self.crypto_key)
        try:
            fernet.decrypt(init_word)
            return True
        except cryptography.exceptions.InvalidSignature:
            return False



