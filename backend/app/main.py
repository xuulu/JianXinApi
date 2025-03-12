from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.core.config import DEBUG, settings
from app.core import init_app
from app.urls import register_routers

app = FastAPI(
    debug=DEBUG,
    title=settings.project_title,
    description=settings.project_description,
    version=settings.project_version,
    openapi_url=None,
    docs_url=None,
    redoc_url=None,

    default_response_class=ORJSONResponse
)

init_app.init_db(app)
init_app.init_middlewares(app)
init_app.init_error(app)

register_routers(app)






@app.get("api/web-api")
async def frontEndInterface():
    openapi_json = app.openapi()

    # 去除不是以 /api/v1 开头的路由
    openapi_json["paths"] = {
        path: path_item
        for path, path_item in openapi_json["paths"].items()
        if path.startswith("/api/v1")
    }

    if "components" in openapi_json:
        del openapi_json["components"]

    # 去除没用信息
    for path, path_item in openapi_json["paths"].items():
        for method, operation in path_item.items():
            if "responses" in operation:
                del operation["responses"]

            if "operationId" in operation:
                del operation["operationId"]

            if "tags" in operation:
                del operation["tags"]


    return openapi_json
