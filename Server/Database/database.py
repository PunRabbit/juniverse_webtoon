import asyncio
import aiomysql
import datetime
import pymysql
from Server.Config.config import config_args


class AsyncDB(object):

    def __init__(self):
        self.fetchall = False
        self.is_dict = True

    @classmethod
    async def async_db_call(cls, query):
        db = await aiomysql.connect(host=f'{config_args.DATABASE_ADDRESS}',
                                    port=config_args.DATABASE_PORT_NUMBER,
                                    user=f'{config_args.DATABASE_USER_NAME}',
                                    password=f'{config_args.DATABASE_USER_PASSWORD}',
                                    db=f'{config_args.DATABASE_NAME}',
                                    charset='utf8',
                                    autocommit=True)

        if cls.is_dict is True:
            cur = await db.cursor(aiomysql.DictCursor)
        else:
            cur = await db.cursor()

        await cur.execute(query)

        if cls.fetchall is True:
            data = await cur.fetchall()
        else:
            data = await cur.fetchone()

        await cur.close()
        db.close()
        return data

    @classmethod
    def generator(cls, query_list):
        default_str = f"{asyncio.__name__}.{asyncio.gather.__name__}("
        for query in query_list:
            middle_str = f'{cls.async_db_call.__qualname__}("{query}"),'
            default_str = default_str + middle_str
        if default_str != f"{asyncio.__name__}.{asyncio.gather.__name__}(":
            total_len = len(default_str)
            default_str = default_str[:total_len - 1] + ")"
        return default_str

    @classmethod
    async def starter(cls, query_list):
        data = await eval(f"{cls.generator(query_list)}")
        return data

    @classmethod
    def take_result(cls, query_list, q_fetchall=False, q_is_dict=True):
        cls.fetchall = q_fetchall
        cls.is_dict = q_is_dict
        data = asyncio.run(cls.starter(query_list))
        return data


class DatabaseConnector(object):

    @classmethod
    async def get_db_cur(cls):
        db = pymysql.connect(host=f'{config_args.DATABASE_URL}',
                             port=config_args.DATABASE_PORT_NUMBER,
                             user=f'{config_args.DATABASE_USER_NAME}',
                             passwd=f'{config_args.DATABASE_USER_PASSWORD}',
                             db=f"{config_args.DATABASE_NAME}",
                             charset='utf8',
                             autocommit=True)
        return db, db.cursor()


class DatabaseKeyChecker(DatabaseConnector):

    @classmethod
    async def check_crypto_key(cls) -> str:
        db, cursor = cls.get_db_cur()
        sql = "SELECT key_id FROM secret_key WHERE key_name = 'crypto'"
        cursor.execute(sql)
        data: list = cursor.fetchall()
        if len(data) == 0:
            return "None"
        else:
            return data[0][0]


class DatabaseKeySaver(DatabaseConnector):

    @classmethod
    async def save_crypto_key(cls, key: str):
        current_time = str(datetime.datetime.now())
        sql_query = f"INSERT INTO secret_key (key_name, key_value, update_date)" \
                    f"SELECT 'crypto', '{key}', '{current_time}' FROM DUAL WHERE NOT EXISTS" \
                    f"(SELECT key_id FROM secret_key WHERE key_name = 'crypto')"
        db, cursor = await cls.get_db_cur()
        cursor.execute(sql_query)
        db.commit()

    @classmethod
    async def save_bcrypt_key(cls, key: str):
        current_time = str(datetime.datetime.now())
        sql_query = f"INSERT INTO secret_key (key_name, key_value, update_date)" \
                    f"VALUES ('bcrypt', '{key}', '{current_time}') FROM DUAL WHERE NOT EXISTS" \
                    f"(SELECT key_id FROM secret_key WHERE key_name = 'bcrypt')"
        db, cursor = await cls.get_db_cur()
        cursor.execute(sql_query)
        db.commit()

    @classmethod
    async def save_server_key(cls, key: str):
        current_time = str(datetime.datetime.now())
        sql_query = f"INSERT INTO secret_key (key_name, key_value, update_date)" \
                    f"VALUES ('server', '{key}', '{current_time}') FROM DUAL WHERE NOT EXISTS" \
                    f"(SELECT key_id FROM secret_key WHERE key_name = 'server')"
        db, cursor = cls.get_db_cur()
        cursor.execute(sql_query)
        db.commit()


class DatabaseKeyLoader(DatabaseConnector):

    @classmethod
    async def load_crypto_key(cls):
        sql_query = f"SELECT key_id, key_value FROM secret_key WHERE key_name = crypto"
        db, cursor = cls.get_db_cur()
        cursor.execute(sql_query)
        return cursor.fetchall()

    @classmethod
    async def load_bcrypt_key(cls):
        sql_query = f"SELECT key_id, key_value FROM secret_key WHERE key_name = bcrypt"
        db, cursor = cls.get_db_cur()
        cursor.execute(sql_query)
        return cursor.fetchall()

    @classmethod
    async def load_server_key(cls):
        sql_query = f"SELECT key_id, key_value FROM secret_key WHERE key_name = server"
        db, cursor = cls.get_db_cur()
        cursor.execute(sql_query)
        return cursor.fetchall()
