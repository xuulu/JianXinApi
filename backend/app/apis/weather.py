from . import url, http, cache





@url.get('/weather', status_code=200)
async def weather(q: str):
    # 过滤掉后缀
    if any(substring in q for substring in ['市', '县', '区', '自治州', '旗', '自治县', '市辖区', '特区', '林区']):
        return {
            'title': '天气查询',
            "error": "未找到该城市!",
            "detail": [
                {
                    "loc": ['市', '县', '区', '自治州', '旗', '自治县', '市辖区', '特区', '林区'],
                    "msg": "请去掉后缀，例如：'北京市' -> '北京'"
                }
            ]
        }

    # 缓存
    weather = await cache.get('weather')
    if weather is None:
        response = await http.get('https://weather.cma.cn/api/map/weather/1')
        cities = response.json().get('data', {}).get('city', [])
        weather = {}
        for city in cities:
            weather[city[1]] = city[0]

        await cache.set('weather', weather)


    id = weather.get(q, None)
    print(id)

    if id is None: return {'title': '天气查询', 'error': '未找到该城市'}

    response = await http.get(f'https://weather.cma.cn/api/now/{id}')

    return {
        'title': '天气查询',
        'data': response.json()['data']
    }
