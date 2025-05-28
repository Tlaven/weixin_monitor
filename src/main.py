import asyncio
from concurrent.futures import ThreadPoolExecutor
from core.window_manager import WindowsWindowManager
from core.image_processor import ImageProcessor
from core.ai_analyzer import DashscopeAnalyzer
from core.chat_monitor import ChatMonitor
from core.ocr_processor import OCRProcessor
from services.screenshot_service import ScreenshotService
from services.analysis_service import AnalysisService
from services.alert_service import AlertService
from config.config import CONFIG
from utils.logger import LOGGER
from utils.file_utils import save_image

async def monitor_chat():
    """主监控循环"""
    window_manager = WindowsWindowManager()
    image_processor = ImageProcessor()
    ai_analyzer = DashscopeAnalyzer(base_url=CONFIG.get("ai.base_url"))
    chat_monitor = ChatMonitor(CONFIG.get("thresholds.change_detection"))
    ocr_processor = OCRProcessor(CONFIG.get("paths.ocr_results"))
    screenshot_service = ScreenshotService(window_manager, image_processor)
    analysis_service = AnalysisService(ai_analyzer, image_processor)
    alert_service = AlertService()

    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        while True:
            try:
                screenshot = screenshot_service.capture_chat_region()
                if chat_monitor.check_updates(screenshot):
                    LOGGER.info("New chat message detected")
                    screenshot_chat = screenshot_service.capture_details()
                    if screenshot_chat:
                        chat_text = ocr_processor.extract_text(screenshot_chat)
                        result = await loop.run_in_executor(
                            pool, lambda: asyncio.run(analysis_service.analyze_text(chat_text))
                        )
                        if result:
                            save_image(screenshot_chat, CONFIG.get("paths.judgments"))
                            alert_service.play_alert()
                await asyncio.sleep(CONFIG.get("app.polling_interval"))
            except Exception as e:
                LOGGER.error(f"Error in monitor loop: {e}")
                await asyncio.sleep(CONFIG.get("app.polling_interval"))

def start_monitor():
    """启动监控"""
    try:
        asyncio.run(monitor_chat())
    except KeyboardInterrupt:
        LOGGER.info("Monitoring stopped by user")

LOGGER.info("New chat message detected")
if __name__ == "__main__":
    start_monitor()