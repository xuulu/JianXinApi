from . import url, http


@url.get('/ys_kaci', status_code=200)
async def ys_kaci():
    # 米游社表情包
    'https://bbs-api-static.miyoushe.com/misc/api/emoticon_set'
    response_content = await http.get('https://api-takumi.mihoyo.com/common/blackboard/ys_obc/v1/gacha_pool?app_sn=ys_obc')
    response = response_content.json()
    return {
        "title": "原神卡池信息",
        'list': [
            {
                "title": response['data']['list'][0]['title'],
                "content": response['data']['list'][0]['content_before_act'],
                "icon": response['data']['list'][0]['pool'][0]['icon'],
            },
            {
                "title": response['data']['list'][1]['title'],
                "content": response['data']['list'][1]['content_before_act'],
                "icon": response['data']['list'][1]['pool'][0]['icon'],
            },
        ],
        "start_time": response['data']['list'][0]['start_time'],
        "end_time": response['data']['list'][0]['end_time']
    }