from . import url, http, RedirectResponse
import random


@url.get('/mishe_cos', status_code=200)
async def mishe_cos(top: bool = False, new: bool = False, type='json'):
    if top:
        url = 'https://bbs-api.miyoushe.com/post/wapi/getImagePostTopN'
        params = {
            'forum_id': '49',
            'gids': '1',
        }
    elif new:
        url = 'https://bbs-api.miyoushe.com/post/wapi/getForumPostList'
        params = {
            'forum_id': '49',
            'gids': '2',
            'is_good': 'false',
            'is_hot': 'false',
            'page_size': '20',
            'sort_type': '2',
        }
    else:
        return {
            "error": "请检查参数是否正确",
            "detail": [
                {
                    "loc": ['top', 'new'],
                    "msg": "loc中的查询参数必须二选一"
                }
            ]
        }

    response = await http.get(url, params=params)

    data_list = response.json()['data']['list']
    data = [
        {
            "title": item['post']['subject'],  # .encode("utf-8"),
            "coser": item['user']['nickname'],  # .encode("utf-8"),
            "images": [img['url'] for img in item['image_list']]
        }
        for item in data_list
    ]

    if type == 'image':
        return RedirectResponse(random.choice(random.choice(data)['images']))

    return {
        'title': '米社cos',
        'data': data
    }
