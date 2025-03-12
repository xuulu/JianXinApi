from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

# 导入应用配置和初始化相关模块
from app.core.config import DEBUG, settings
from app.core import init_app
from app.urls import register_routers

# 创建FastAPI应用实例，并配置基本参数
app = FastAPI(
    debug=DEBUG,  # 调试模式
    title=settings.project_title,  # 项目标题
    description=settings.project_description,  # 项目描述
    version=settings.project_version,  # 项目版本
    openapi_url=None,  # 关闭OpenAPI规范文档的URL
    docs_url=None,  # 关闭交互式API文档的UR
    redoc_url=None,  # 关闭Redoc风格API文档的URL

    default_response_class=ORJSONResponse  # 设置默认响应类为ORJSONResponse，以提高性能
)

# 初始化数据库
init_app.init_db(app)
# 初始化中间件
init_app.init_middlewares(app)
# 初始化错误处理
init_app.init_error(app)

# 注册路由
register_routers(app)




