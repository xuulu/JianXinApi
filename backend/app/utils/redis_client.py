from fastapi import FastAPI
from fastapi.responses import RedirectResponse


from redis import asyncio as aioredis
import orjson
from typing import Optional, Callable
from functools import wraps
from app.core.logger import logger
from app.core.config import settings


class RedisClient:
    def __init__(
            self,
            redis_url: str,
            *,
            redis_expire=None,
            max_connections: int = 10,
            serializer=orjson.dumps,  # 默认使用 orjson 进行序列化
            deserializer=orjson.loads  # 默认使用 orjson 进行反序列化
    ):
        self.redis_expire = redis_expire if redis_expire is not None else settings.redis_expire

        self.serializer = serializer
        self.deserializer = deserializer

        self._redis = aioredis.from_url(
            redis_url,
            decode_responses=True,  # 自动解码为字符串
            max_connections=max_connections,
            encoding='utf-8'
        )

    async def close(self) -> None:
        """关闭 Redis 连接"""
        await self._redis.disconnect()


    # 封装常用操作
    async def set(self, key: str, value: str, expire: int = None):
        redis = self._redis
        try:
            value = self.serializer(value)  # 序列化数据
        except Exception as e:
            logger.error(f"序列化数据时出错: {e}")
            logger.error(f"正在使用原始数据缓存")

        if expire is None: expire = self.redis_expire
        await redis.set(key, value, ex=expire)

    async def get(self, key: str):
        redis = self._redis
        value = await redis.get(key)
        if value is not None:
            try:
                return self.deserializer(value)  # 反序列化数据
            except Exception as e:
                logger.error(f"反序列化数据时出错: {e}")
                logger.error(f"正在使用原始数据")
                return value
        return None

    async def delete(self, key: str):
        redis = self._redis
        await redis.delete(key)



cache = RedisClient(settings.redis_host)

def init_redis_client(app: FastAPI):
    @app.on_event("startup")
    async def init_redis() -> None:
        logger.info('正在连接redis...')

    @app.on_event("shutdown")
    async def close_redis() -> None:
        logger.info('断开redis连接...')
        await cache.close()


