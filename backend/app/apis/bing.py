from . import url, http, RedirectResponse


@url.get(
    '/bing',
    name='必应一图',
    summary="获取必应每日一图",  # 接口列表中的简短描述
    description="### 详细说明",  # 支持 Markdown 的详细说明
    response_description="返回 JSON 数据",
    tags=[""],  # 分组标签
    status_code=200
)
async def bing(type: str = 'json'):
    response = await http.get('http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1')
    url = f'http://cn.bing.com{response.json()['images'][0]['url']}'
    print('cs一下')
    if type == 'image':
        return RedirectResponse(url)

    return {
        'title': 'bing每日一图',
        'image': url
    }
