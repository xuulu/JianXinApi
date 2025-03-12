from lxml import html, etree
import orjson

from . import url, http

def round_to_str(value: int) -> str:
    """
    将输入值四舍五入到最近的万位、千位、百位、十位或个位
    """
    try:
        # 尝试将输入转换为整数
        num = int(value)
    except ValueError:
        raise logger.error("输入必须是数字或可转换为数字的字符串")

    if num >= 10000:
        # 四舍五入到万位
        rounded_num = f'{round(num / 10000)} 万'
    elif num >= 1000:
        # 四舍五入到千位
        rounded_num = f'{round(num / 1000)} 千'
    else:
        rounded_num = num

    return rounded_num


@url.get('/hot_search', status_code=200)
async def hot_search(q):
    # 定义列表
    list = []

    if q in ['抖音', 'douyin']:
        headers = {
            'referer': 'https://www.douyin.com/hot',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
        }
        response = await http.get('https://www.douyin.com/aweme/v1/web/hot/search/list', headers=headers)
        # 循环
        for index, item in enumerate(response.json()['data']['word_list']):
            list.append(
                f"{index + 1}、{item['word']}(当前热度:{round_to_str(item['hot_value'])})"
            )

    elif q in ['快手', 'kuaishou']:
        headers = {
            'referer': 'https://cn.bing.com/',
            'host': 'www.kuaishou.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
        }
        response = await http.get('https://www.kuaishou.com/brilliant', headers=headers)

        # 解析 HTML
        tree = html.fromstring(response.text)
        # 提取包含 Apollo 状态的 script 标签内容
        script_text = tree.xpath('//script[contains(., "__APOLLO_STATE__")]/text()')[0]
        # 提取纯净 JSON（处理 JavaScript 赋值）
        json_str = script_text.split("window.__APOLLO_STATE__=", 1)[1].rsplit(";(function()", 1)[0].strip()
        print(json_str)
        # 解析为 Python 字典
        apollo_data = orjson.loads(json_str)
        # 获取数据列表
        ks_items = apollo_data['defaultClient']['$ROOT_QUERY.visionHotRank({"page":"brilliant"})']['items']

        for index, item in enumerate(ks_items):
            item_id = item["id"]
            hot_item = apollo_data['defaultClient'].get(item_id, {})
            name = hot_item.get("name")
            hot_value = hot_item.get("hotValue")
            list.append(
                f"{index + 1}、{name}(当前热度:{hot_value})"
            )






    elif q in ['头条', 'toutiao']:
        response = await http.get('https://is-lq.snssdk.com/api/suggest_words/?business_id=10016')
        for index, item in enumerate(response.json()['data'][0]['words']):
            list.append(
                f"{index + 1}、{item['word']}(当前热度:{round_to_str(item['params']['fake_click_cnt'])})"
            )

    elif q in ['知乎', 'zhihu']:
        response = await http.get('https://www.zhihu.com/billboard')

        tree = html.fromstring(response.text)
        items = tree.xpath('//div[@class="HotList-itemBody"]')

        list = [
            f"{index + 1}、{item.xpath('.//div[contains(@class, \"HotList-itemTitle\")]/text()')[0].strip()}"
            f" ({item.xpath('.//div[contains(@class, \"HotList-itemMetrics\")]/text()')[0].strip()})"
            for index, item in enumerate(items)
        ]

    elif q in ['百度', 'baidu']:
        response = await http.get('https://top.baidu.com/board?tab=realtime')

        tree = html.fromstring(response.text)
        items = tree.xpath('//div[@class="category-wrap_iQLoo horizontal_1eKyQ"]')

        list = [
            f"{index + 1}、{item.xpath('.//div[contains(@class, \"c-single-text-ellipsis\")]/text()')[0].strip()}"
            f" (当前热度:{round_to_str(item.xpath('.//div[contains(@class, \"hot-index_1Bl1a\")]/text()')[0].strip())})"
            for index, item in enumerate(items)
        ]

    elif q in ['微博', 'weibo']:
        response = await http.get('https://weibo.com/ajax/side/hotSearch')
        for index, item in enumerate(response.json()['data']['realtime']):
            list.append(f"{index + 1}、{item['word']} (当前热度:{round_to_str(item['num'])})")

    elif q in ['b站', '哔哩哔哩', 'bilibili']:
        response = await http.get('https://app.bilibili.com/x/v2/search/trending/ranking?limit=50')
        for index, item in enumerate(response.json()['data']['list']):
            list.append(f"{index + 1}、{item['keyword']} (当前热度:{round_to_str(item['hot_id'])})")

    else:
        return {'title': '热搜榜单', 'error': '暂不支持该平台'}

    return {'title': q, 'data': list}
