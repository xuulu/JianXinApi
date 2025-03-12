from fastapi import APIRouter
from tortoise.expressions import Q
from tortoise.contrib.pydantic import pydantic_model_creator
from typing import List
from app.models.frontEnd import ApiList

url = APIRouter()

ApiListPydantic = pydantic_model_creator(ApiList, name="ApiList")


# 查询所有
@url.get(
    "",
    response_model=List[ApiListPydantic],
    summary="获取所有简心API接口",
    status_code=200
)
async def get_all_api_lists():
    # 返回数据库中所有API接口列表，按照ID进行递增排序
    return await ApiList.all().order_by('id')



@url.get(
    "/search/",
    response_model=List[ApiListPydantic],
    summary="模糊搜索接口接口",
    status_code=200
)
async def search_apilists(q: str = None, ):
    """
    模糊搜索接口列表

    参数：
    - q: 搜索关键词（支持名称、路径、介绍字段）
    """
    if not q:
        return []

    query = ApiList.filter(
        Q(name__icontains=q) |
        Q(path__icontains=q) |
        Q(introduce__icontains=q)
    )

    # 添加分页功能
    return await query.all().order_by('id')


# 根据ID查询单个接口
@url.get(
    "/{id}/",
    response_model=ApiListPydantic,
    summary="查询单个id接口",
    status_code=200
)
async def get_apilist(id: int):
    """
    根据ID获取API列表信息。

    参数:
    - id (int): 需要查询的API列表的ID。

    返回:
    - ApiListPydantic: 包含所查询ID的API列表信息的响应模型。
    """
    return await ApiList.get(id=id)

