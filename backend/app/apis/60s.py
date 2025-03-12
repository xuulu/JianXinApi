from . import url, http


from datetime import datetime


@url.get("/everyday_60s", status_code=200)
async def yiyan():
    # 获取当前日期并格式化为 'YYYY-MM-DD'
    today = datetime.now().strftime('%Y/%m/%d').replace('/', '-')
    urls = [
        f"https://raw.githubusercontent.com/vikiboss/60s-static-host/main/static/60s/{today}.json",
        f"https://60s-static.viki.moe/60s/{today}.json",
        f"https://cdn.jsdelivr.net/gh/vikiboss/60s-static-host/static/60s/{today}.json"
    ]
    for url in urls:
        try:
            response = await http.get(url)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error: {e}")




