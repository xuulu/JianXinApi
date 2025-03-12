from . import url, http, RedirectResponse
from lxml import html
from urllib.parse import unquote
import orjson

@url.get('/changya', status_code=200)
async def changya(type: str = 'json'):
    response = await http.get('https://m.api.singduck.cn/user-piece/6oGNUeM16kBuRmPct?userId=2003919010')

    tree = html.fromstring(response.text)
    script = tree.xpath('//script[@id="__NEXT_DATA__"]')

    if not script:
        raise ValueError("未找到 <script id='__NEXT_DATA__'> 标签")

    json_str = script[0].text_content()
    json_data = orjson.loads(str(json_str))
    one = json_data["props"]["pageProps"]["pieces"][0]
    artist = one["artist"]  # 艺人
    avatarUrl = one["avatarUrl"]  # 艺人头像
    audioUrl = unquote(one["audioUrl"])  # 歌曲链接
    lyric = one["lyric"]  # 歌词
    
    for type in ['musics', 'mp3']:
        return RedirectResponse(audioUrl)

    return {'title': '随机唱鸭', 'data': {
        'artist': artist,
        'avatarUrl': avatarUrl,
        'audioUrl': audioUrl,
        'lyric': lyric
    }}
