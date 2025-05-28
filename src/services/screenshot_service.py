from PIL import Image
from typing import Optional
from core.window_manager import WindowManager
from core.image_processor import ImageProcessor
from config.config import CONFIG
from utils.logger import LOGGER

import time

class ScreenshotService:
    def __init__(self, window_manager: WindowManager, image_processor: ImageProcessor):
        self.window_manager = window_manager
        self.image_processor = image_processor
        self.window_title = CONFIG.get("app.window_title")
        self.details_title = CONFIG.get("app.details_window_title")
        self.chat_box = CONFIG.get("chat_box")

    def capture_chat_region(self) -> Optional[Image.Image]:
        """截取聊天框区域"""
        window_info = self.window_manager.find_window(self.window_title)
        if not window_info:
            return None
        region = (
            self.chat_box["x"],
            window_info["height"] + self.chat_box["y_offset"],
            self.chat_box["width"],
            self.chat_box["height"]
        )
        screenshot = self.window_manager.capture_screenshot(window_info["hwnd"], region)
        return screenshot

    def capture_details(self) -> Optional[Image.Image]:
        """Capture details window and return the screenshot image."""
        window_info = self.window_manager.find_window(self.window_title)
        if not window_info:
            LOGGER.error("Main window not found")
            return None

        # Calculate center of chat box region for clicking
        click_x = self.chat_box["x"] + self.chat_box["width"] // 2
        click_y = window_info["height"] + self.chat_box["y_offset"] + self.chat_box["height"] // 2
        self.window_manager.simulate_click(window_info["hwnd"], click_x, click_y)

        # Wait for details window to appear
        time.sleep(0.5)
        details_info = self.window_manager.find_window(self.details_title)
        if not details_info:
            LOGGER.error("Details window not found")
            return None

        # Capture screenshot of details window
        screenshot: Image.Image = self.window_manager.capture_screenshot(details_info["hwnd"])
        if not screenshot:
            LOGGER.error("Failed to capture details screenshot")
            return None

        # Convert to grayscale
        screenshot = screenshot.convert("L")
        LOGGER.info("Captured and converted details screenshot to grayscale")

        screenshot_path = self.image_processor.save_image(
            screenshot, CONFIG.get("paths.screenshots"), grayscale=True
        )

        # Close details window
        self.window_manager.simulate_click(details_info["hwnd"], details_info["width"] - 20, 20)
        time.sleep(0.5)  # Wait for close to complete

        # Verify details window is closed
        if self.window_manager.find_window(self.details_title):
            LOGGER.warning("Details window still open")
            return None

        # Click blank area to restore UI
        blank_x = self.chat_box["x"] + self.chat_box["width"]
        blank_y = window_info["height"] - 300
        LOGGER.debug(f"Clicking blank area at ({blank_x}, {blank_y}) to restore UI")
        self.window_manager.simulate_click(window_info["hwnd"], self.chat_box["x"], blank_y)

        return screenshot