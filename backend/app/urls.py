from fastapi import FastAPI
from app.core.config import settings
from app.apis import url as apis_url
from app.frontEnd_api import api_list, api_link, statement

# 路由版本 V1
version = f"v{settings.project_version}"
def register_routers(app: FastAPI):
    app.include_router(apis_url, prefix="/api", tags=["简心API接口"])

    app.include_router(api_list.url, prefix=f"/api/{version}/api-list", tags=["简心API前端接口-接口列表"])
    app.include_router(statement.url, prefix=f"/api/{version}/api-list", tags=["简心API前端接口-网站声明"])
    app.include_router(api_link.url, prefix=f"/api/{version}/friend-links", tags=["简心API前端接口-友链列表"])