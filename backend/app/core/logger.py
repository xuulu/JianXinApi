
from datetime import datetime
from pathlib import Path
from typing import Callable

from loguru import logger
from .config import BASE_DIR


class Logger:
    def __init__(
            self,
            log_path: str = "logs",
            rotation: str = "1 day",
            retention: str = "30 days",
            log_level: str = "INFO",    # 写入文件的日志级别
            enable_console: bool = True
    ):
        """
        初始化日志记录器
        :param log_path: 日志文件存储路径
        :param rotation: 日志轮转周期
        :param retention: 日志保留时间
        :param log_level: 日志记录级别
        :param enable_console: 是否启用控制台日志
        """
        self.log_path = Path(log_path)
        self._configure_logger(rotation, retention, log_level, enable_console)

    def _configure_logger(self, rotation, retention, log_level, enable_console):
        """配置loguru日志记录器"""
        # 确保日志目录存在
        self.log_path.mkdir(parents=True, exist_ok=True)

        # 移除默认配置
        logger.remove()

        # 控制台日志格式
        console_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        )

        # 文件日志格式（包含更多细节）
        file_format = (
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
            "{level: <8} | "
            "{name}:{function}:{line} - {message}"
        )

        if enable_console:
            logger.add(
                sink=lambda msg: print(msg, end=""),  # 兼容uvicorn的日志输出
                format=console_format,
                # level=log_level,
                level='INFO',
                colorize=True
            )

        # 添加文件日志
        logger.add(
            sink=str(self.log_path / "{time:YYYY-MM-DD}.log"),
            rotation=rotation,
            retention=retention,
            format=file_format,
            level=log_level,
            encoding="utf-8",
            backtrace=True,  # 显示异常堆栈
            diagnose=True  # 显示变量值
        )



Logger(
    log_path=BASE_DIR / "logs",
    log_level="ERROR"
)

__all__ = ["logger"]
