# 提示服务

from utils.logger import LOGGER

class AlertService:
    def play_alert(self):
        """播放提示音"""
        try:
            from pygame import mixer
            mixer.init()
            # 使用系统默认提示音或自定义音效
            mixer.Sound("alert.wav").play()  # 需要提供alert.wav文件
            LOGGER.info("Played alert sound")
        except Exception as e:
            LOGGER.error(f"Failed to play alert: {e}")