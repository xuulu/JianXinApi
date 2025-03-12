import random

from app.models.cos import CosVideo,CosImage
from app.core.logger import logger
from app.core.config import settings
from . import url, http, RedirectResponse,cache




async def get_sql_data(model, field):
    """缓存模型的行数，然后返回随机一行数据"""

    key = f'{model.__name__}_count'
    count = await cache.get(key)


    if count is None:
        count = await model.all().count()
        logger.info(f'缓存{key}数据，共{count}条')
        await cache.set(key, count, settings.redis_expire)

    values = await model.filter(id=random.randint(1, int(count))).values(field)
    # 获取第一条数据的某个字段
    return values[0][field]


@url.get('/cos',status_code=200)
async def cos(
        cos_image: bool = False,
        cos_video: bool = False,
        type: str = 'json'
):
    if cos_image:
        data = f'https://cdn.cdnjson.com/pic.html?url={await get_sql_data(CosImage,'url')}'


    elif cos_video:
        data = await get_sql_data(CosVideo,'url')

    else:
        return {
            "error": "请检查参数是否正确",
            "detail": [
                {
                    "loc": ['cos_image', 'cos_video'],
                    "msg": "loc中的查询参数必须二选一"
                }
            ]
        }

    if type in ['image', 'video']:
        print('url', data)
        return RedirectResponse(data)

    return {'title': '逆天cos', 'url': data}



