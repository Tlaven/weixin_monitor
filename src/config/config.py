# 配置管理

import yaml
import os
from utils.logger import LOGGER

class Config:
    """管理配置文件加载和访问"""
    def __init__(self, config_path="config.yaml"):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f)
            LOGGER.info(f"Loaded configuration from {config_path}")
        except Exception as e:
            LOGGER.error(f"Failed to load config: {e}")
            raise

    def get(self, key, default=None):
        """获取配置值，支持嵌套键（如 'ai.model'）"""
        keys = key.split(".")
        value = self.config
        for k in keys:
            value = value.get(k, default)
            if value == default:
                break
        return value

CONFIG = Config()