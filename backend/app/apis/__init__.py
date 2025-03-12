from fastapi import APIRouter
from fastapi.responses import RedirectResponse

"""用于项目的功能模块"""
from app.core.logger import logger
from app.core.response import JsonResponse
from app.utils.http_client import http
from app.utils.redis_client import cache

__all__ = [
    "logger",
    "http",
    "cache",
    "RedirectResponse",
]

url = APIRouter(default_response_class=JsonResponse)

import importlib
from pathlib import Path

for file in Path(__file__).parent.glob("*.py"):
    if file.stem not in ["__init__", "utils"]:  # 忽略 __init__.py 和 utils.py
        print(f"正在导入 {file.stem}...")
        importlib.import_module(f".{file.stem}", package=__name__)
