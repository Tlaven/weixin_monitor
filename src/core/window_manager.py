# 窗口操作与截图接口

from abc import ABC, abstractmethod
from typing import Optional, Tuple
import win32gui
import win32con
import win32api
import win32ui
import ctypes
from PIL import Image
from utils.logger import LOGGER

class WindowManager(ABC):
    @abstractmethod
    def find_window(self, title: str) -> dict:
        """查找窗口，返回句柄和位置信息"""
        pass

    @abstractmethod
    def capture_screenshot(self, hwnd, region: Optional[Tuple] = None) -> Image.Image:
        """截取窗口或指定区域"""
        pass

    @abstractmethod
    def simulate_click(self, hwnd, x: int, y: int) -> None:
        """模拟鼠标点击"""
        pass

class WindowsWindowManager(WindowManager):
    def find_window(self, title: str) -> Optional[dict]:
        """查找Windows窗口"""
        hwnd = win32gui.FindWindow(None, title)
        if hwnd == 0:
            # LOGGER.error(f"Window not found: {title}")
            return None
        rect = win32gui.GetWindowRect(hwnd)
        info = {
            "hwnd": hwnd,
            "x": rect[0],
            "y": rect[1],
            "width": rect[2] - rect[0],
            "height": rect[3] - rect[1]
        }
        LOGGER.debug(f"Found window {title}: {info}")
        return info

    def capture_screenshot(self, hwnd, region: Optional[Tuple] = None) -> Optional[Image.Image]:
        """使用PrintWindow截取窗口"""
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top

        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        saveDC.SelectObject(saveBitMap)

        result = ctypes.windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        im: Image.Image = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)

        if result != 1:
            LOGGER.error("Screenshot failed")
            return None

        if region:
            x, y, w, h = region
            im = im.crop((x, y, x + w, y + h))
        # LOGGER.info("Captured screenshot")
        return im

    def simulate_click(self, hwnd, x: int, y: int) -> None:
        """模拟后台点击"""
        lParam = win32api.MAKELONG(x, y)
        win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)
        LOGGER.debug(f"Simulated click at ({x}, {y})")