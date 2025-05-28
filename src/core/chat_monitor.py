import cv2
import numpy as np
from typing import Optional
from PIL import Image
from utils.logger import LOGGER
import time

class ChatMonitor:
    def __init__(self, change_threshold: int):
        self.previous_screenshot = None
        self.change_threshold = change_threshold
        self.last_update_time = 0
        self.debounce_interval = 10  # 秒，忽略10秒内的重复更新

    def check_updates(self, current_screenshot: Optional[Image.Image]) -> bool:
        """检查聊天内容是否更新，带防抖机制"""
        if not current_screenshot:
            LOGGER.warning("No screenshot provided")
            return False

        # 防抖：忽略短时间内的重复更新
        if time.time() - self.last_update_time < self.debounce_interval:
            LOGGER.debug("Debouncing: too soon since last update")
            return False

        screenshot_cv = cv2.cvtColor(np.array(current_screenshot), cv2.COLOR_RGB2BGR)
        
        if self.previous_screenshot is None:
            self.previous_screenshot = screenshot_cv
            LOGGER.debug("Stored initial screenshot")
            return False

        diff = cv2.absdiff(screenshot_cv, self.previous_screenshot)
        gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        non_zero_count = np.count_nonzero(gray_diff)
        LOGGER.debug(f"Pixel difference: {non_zero_count}")

        if non_zero_count > self.change_threshold:
            # LOGGER.info(f"Detected chat update (diff: {non_zero_count})")
            self.previous_screenshot = screenshot_cv
            self.last_update_time = time.time()
            return True

        LOGGER.debug("No chat update detected")
        return False