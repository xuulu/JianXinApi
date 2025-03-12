from fastapi import APIRouter

url = APIRouter()

friendshipLinkList = [
    {
        "name": "简心API",
        "url": "https://api.qvqa.cn/",
        "icon": "https://www.qvqa.cn/favicon.ico",
        "description": "安全可靠的接口服务平台",
        "email": "1634964@qq.com",
    },
]


@url.get("", summary="获取友链列表接口", status_code=200)
async def get_friend_links():
    return friendshipLinkList


@url.get("/statements", summary="获取友链申请、条件和格式接口", status_code=200)
async def friend_links_statements():
    list = [
        '1.请做好本站友链，再进行申请。',
        '2.本站谢绝收录非API接口服务类网站。',
        '3.需包含但不限于免费内容，谢绝收录广告类网站。',
        '4.严禁违法、违规、违德网站，优先考虑备案域名。',
    ]
    format = {
        "name": "简心API",
        "url": "https://api.qvqa.cn/",
        # "icon":"http://q.qlogo.cn/headimg_dl?dst_uin=1634964&spec=640&img_type=jpg",
        "icon": "https://www.qvqa.cn/favicon.ico",
        "description": "安全可靠的接口服务平台",
        "email": "1634964@qq.com",
    }

    return {
        "title": "简心API - 友链申请",
        "data": list,
        "format": format,
        "questionnaire": 'https://wj.qq.com/s2/18784608/110d/',  # 填写问卷链接
    }
