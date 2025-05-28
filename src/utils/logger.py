# 日志记录

from loguru import logger
import os

def setup_logger():
    """配置日志记录"""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "app.log")
    
    # 添加文件日志输出
    logger.add(log_file, rotation="10 MB", level="INFO", format="{time} - {level} - {message}")
    
    return logger

LOGGER = setup_logger()