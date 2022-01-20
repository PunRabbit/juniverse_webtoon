import asyncio
import aiomysql
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
