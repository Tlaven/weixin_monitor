# 文件操作

import os
import shutil
from typing import Optional
from datetime import datetime
from utils.logger import LOGGER

def save_image(image, folder: str, grayscale: bool = False) -> Optional[str]:
    """保存图像到指定文件夹，返回文件路径"""
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    filepath = os.path.join(folder, filename)
    
    try:
        if grayscale:
            image = image.convert("L")
        image.save(filepath)
        LOGGER.info(f"Saved image to {filepath}")
        return filepath
    except Exception as e:
        LOGGER.error(f"Failed to save image: {e}")
        return None

def copy_image(src_path: str, dest_folder: str) -> bool:
    """复制图像到目标文件夹"""
    os.makedirs(dest_folder, exist_ok=True)
    try:
        shutil.copy(src_path, dest_folder)
        LOGGER.info(f"Copied image from {src_path} to {dest_folder}")
        return True
    except Exception as e:
        LOGGER.error(f"Failed to copy image: {e}")
        return False