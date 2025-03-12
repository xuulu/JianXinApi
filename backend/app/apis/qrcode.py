from . import url, http
from fastapi.responses import Response
from urllib.parse import quote

@url.get('/qrcode', status_code=200)
async def qrcode(
        q: str,
        color: str = 'A2007C',
        bgcolor:str= '00B2BF',
        size:int=400
):


    url = (f'https://qrcode.hlcode.cn/beautify/style/create?'
           f'bgColor={quote(bgcolor)}&bodyType=1'
           f'&content={q}'
           f'&down=0&embedPosition=0&embedText=&embedTextColor=%23000000&embedTextSize=38&eyeInColor=%23000000&eyeOutColor=%23000000&eyeType=8&eyeUseFore=1&fontFamily=0'
           f'&foreColor={quote(color)}&foreColorImage=&foreColorTwo=&foreType=0&frameColor=&gradientWay=0&level=H&logoShadow=0&logoShap=2&logoUrl=&margin=2&rotate=30'
           f'&size={size}&format=1&qrCodeId=0')

    response = await http.get(url)
    response = await http.get(response.json()['data'])

    return Response(content=response.content,media_type = "image/jpeg")
