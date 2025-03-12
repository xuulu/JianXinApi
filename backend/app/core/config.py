from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

# 是否为 调试模式
DEBUG: bool = True

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    # 项目配置
    project_title: str = Field("简心API", description="项目名称")
    project_description: str = Field("简心API致力于为用户提供安全可靠的接口服务平台", description="项目简介")
    project_version: str = Field("1", description="项目版本")

    # 数据库配置 pgsql
    db_host: str = Field(..., description="数据库地址")
    db_port: int = Field(5432, description="数据库端口")
    db_user: str = Field(..., description="数据库用户名")
    db_password: str = Field(..., description="数据库密码")
    db_database: str = Field(..., description="数据库名")

    db_models: list = Field(
        default=
        [
            'aerich.models',  # 必须
            # 自定义模型:
            'app.models.frontEnd',
            'app.models.cos',

        ],
        description="数据库模型 路径"
    )

    # redis配置
    redis_host: str = Field(..., description="redis地址")
    # 缓存过期时间，单位秒  60*60*1=3600 一小时
    redis_expire: int = Field(3600, description="缓存过期时间，单位秒")

    # 跨域配置
    middlewares_origin: list = Field([
        "http://localhost:5173",  # 允许的前端域名
        "https://api.qvqa.cn",  # 另一个允许的前端域名
    ], description="允许跨域的域名")

    class Config:
        env_file = BASE_DIR / f".env.{'development' if DEBUG else 'production'}"


# 加载配置并处理异常
try:
    settings = Settings()
except Exception as e:
    print(f"加载配置失败: {e}")
