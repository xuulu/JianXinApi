
from fastapi.responses import ORJSONResponse
from typing import Union

# 定义状态码及其描述的字典
status_code_descriptions = {
    200: '请求已成功处理',
    201: '请求已成功处理，并创建了新的资源',
    202: '请求已被接受，但尚未处理完成',
    204: '请求已成功处理，但没有要返回的数据',
    300: '请求的资源有多个可选项，客户端可以选择一个',
    301: '请求的资源已被永久移动到新的URL',
    302: '请求的资源暂时移动到新的URL',
    400: '请求的语法错误，服务器无法理解',
    401: '请求需要身份验证',
    403: '服务器拒绝执行该请求',
    404: '请求的资源在服务器上不存在',
    409: '请求与当前服务器的配置冲突',
    500: '服务器在处理请求时发生了内部错误',
    501: '服务器不支持请求所需的功能',
    502: '服务器作为网关或代理时收到了来自上游服务器的无效响应',
    503: '服务器暂时无法处理请求（可能是由于过载或维护）',
    504: '服务器作为网关或代理时，未及时从上游服务器收到响应',
}


class JsonResponse(ORJSONResponse):
    media_type = "application/json; charset=utf-8"

    def __init__(
            self,
            data: Union[dict, list, str] = None,
            code: int = 200,
            **kwargs
    ):
        super().__init__(
            content={
                "code": code,
                "msg": status_code_descriptions.get(code, '未知错误'),
                "data": data
            },
            status_code=code
        )
