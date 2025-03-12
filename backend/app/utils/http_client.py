from http.client import responses

from fastapi import FastAPI
import httpx
import orjson
from typing import Any
from app.core.logger import logger


class ORJSONResponse(httpx.Response):
    """
        继承自 httpx.Response 的自定义响应类，用于使用 orjson 库解析 JSON 数据。

        该类重写了 json 方法，以实现使用 orjson 解析响应内容，提高解析效率。
    """

    def json(self, **kwargs: Any) -> Any:
        try:
            # 直接解析原始字节（orjson 需要 bytes）
            logger.info('httpx正在使用orjson解析json...')
            return orjson.loads(self.content, **kwargs)
        except orjson.JSONDecodeError as e:
            # 转换为标准库异常类型以保持兼容性
            raise logger.error(f'httpx使用orjson库解析json失败: {e}')


class HttpClient:
    """
    HttpClient 类提供了一个封装了 httpx 客户端的异步 HTTP 客户端实现。
    它支持 HTTP/2，并在请求时自动添加了用户代理头。
    """

    def __init__(self):
        """
        初始化 HttpClient 实例。

        此方法会创建一个 httpx.AsyncClient 实例，并配置其支持 HTTP/2 以及设置默认的用户代理头。
        它还指定了使用 ORJSONResponse 作为响应类，以利用 ORJSON 的高性能解析能力。
        """
        logger.info('正在初始化 httpx 客户端...')
        self._httpx = httpx.AsyncClient(
            http2=True,
            headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
            },
        )

    async def close(self):
        """
        关闭 httpx 客户端。

        此方法确保在使用完 HttpClient 后正确地关闭了 httpx.AsyncClient 实例，以释放资源。
        """
        await self._httpx.aclose()

    async def get(self, url: str, **kwargs) -> httpx.Response:
        """
        发起 GET 请求。

        参数:
        - url: 请求的 URL。
        - **kwargs: 额外的关键字参数，将被传递给 httpx.AsyncClient.get 方法。

        返回:
        - httpx.Response: 请求的响应对象。
        """
        response = await self._httpx.get(url=url, **kwargs)
        response.__class__ = ORJSONResponse
        return response

    async def post(self, url: str, **kwargs) -> httpx.Response:
        """
        发起 POST 请求。

        参数:
        - url: 请求的 URL。
        - **kwargs: 额外的关键字参数，将被传递给 httpx.AsyncClient.post 方法。

        返回:
        - httpx.Response: 请求的响应对象。
        """
        response = await self._httpx.post(url=url, **kwargs)
        response.__class__ = ORJSONResponse  # 动态替换响应类
        return response



http = HttpClient()


def init_http_client(app: FastAPI):
    # @app.on_event("startup")
    # async def init_redis() -> None:
    #     logger.info('正在连接httpx...')
    #     await http.connect()

    @app.on_event("shutdown")
    async def close_redis() -> None:
        logger.info('断开httpx连接...')
        await http.close()
