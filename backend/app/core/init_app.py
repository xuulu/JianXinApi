from fastapi import FastAPI, HTTPException, status
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request

from .logger import logger
from .config import settings


def init_db(app: FastAPI) -> FastAPI:
    logger.info("正在初始化 数据库...")
    from tortoise.contrib.fastapi import register_tortoise

    TORTOISE_ORM: dict = {
        'connections': {
            # 连接的Dict格式
            'default': {
                'engine': 'tortoise.backends.asyncpg',
                'credentials': {
                    'host': settings.db_host,
                    'port': settings.db_port,
                    'user': settings.db_user,
                    'password': settings.db_password,
                    'database': settings.db_database,
                }
            },
            # 使用DB_URL字符串连接,上边二选一
            # 'default': 'postgresql://127.0.0.1:5432/'
        },
        'apps': {
            'models': {
                'models': settings.db_models,
                # 如果未指定default_connection，则默认为“默认”
                'default_connection': 'default',
            }
        },
        "use_tz": False,  # 建议不要开启，不然存储日期时会有很多坑，时区转换在项目中手动处理更稳妥。
        "timezone": "Asia/Shanghai"
    }
    # 初始化 ORM 数据库
    register_tortoise(app,config=TORTOISE_ORM,add_exception_handlers=True)


    from app.utils.redis_client import init_redis_client
    init_redis_client(app)



def init_middlewares(app: FastAPI):
    from fastapi.middleware.cors import CORSMiddleware  # 跨域中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.middlewares_origin,  # 允许的域名列表
        allow_credentials=True,  # 是否允许发送 Cookie
        allow_methods=["*"],  # 允许的 HTTP 方法
        allow_headers=["*"],  # 允许的请求头
    )


def init_error(app: FastAPI) :
    logger.info("正在初始化 异常...")

    # 处理 HTTPException
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        status_code = exc.status_code
        detail = exc.detail

        # 汉化常见错误消息
        chinese_detail = {
            "Not Found": "资源未找到",
            "Forbidden": "拒绝访问",
            "Unauthorized": "未经授权",
            "Bad Request": "无效请求",
        }.get(detail, detail)

        return ORJSONResponse(
            status_code=status_code,
            content={
                "code": status_code,
                "msg": chinese_detail,
                "data": None
            },
        )

    # 处理请求验证错误

    # 集中管理错误消息映射
    ERROR_MAPPING = {
        "Field required": "字段 '{loc}' 是必填项",
        "Input should be a valid boolean, unable to interpret input": "请输入有效的布尔值(true/false)",
        "none is not an allowed value": "字段 '{loc}' 不允许为空",
        "value is not a valid integer": "需要整数类型",
        "value is not a valid float": "需要浮点数类型",
        "Input should be a valid datetime": "请输入有效的日期时间格式",
        "Input should be a valid email": "请输入有效的邮箱格式",
        "string does not match regex": "格式不符合要求",
        "string too short": "长度过短（最少{min_length}位）",
        "string too long": "长度过长（最多{max_length}位）",
        "does not exist": "对象'{loc}'不存在",
    }
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        def process_error(error: dict) -> dict:
            """处理单个错误信息"""
            # 生成字段路径 (body.name → body.name.0 → etc.)
            loc = ".".join(str(loc) for loc in error["loc"] if loc != "body")

            # 获取原始错误信息
            raw_msg = error["msg"]

            # 获取上下文信息（用于长度验证）
            ctx = error.get("ctx")

            # 匹配预定义错误模板
            if raw_msg in ERROR_MAPPING:
                template = ERROR_MAPPING[raw_msg]
                msg = template.format(
                    loc=loc,
                    min_length=ctx.get("min_length") if ctx else None,
                    max_length=ctx.get("max_length") if ctx else None
                )
            else:
                # 未匹配的保留原始信息，并添加定位
                msg = f"[{loc}] {raw_msg}"

            return {"loc": loc, "msg": msg, "type": error["type"]}

        # 处理所有错误
        processed_errors = [process_error(e) for e in exc.errors()]

        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "code": 422,
                "msg": "参数验证失败",
                "errors": processed_errors
            },
        )
