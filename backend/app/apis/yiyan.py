from . import url, http


@url.get("/yiyan", status_code=200)
async def yiyan():
    return {'title': '一言', 'error': '正在维护...'}




