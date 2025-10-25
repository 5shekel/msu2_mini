"""
ContinuousCapture - Screen and Window Capture Utility for Windows

This module provides functionality to capture screenshots continuously at specified intervals.
It supports both full screen capture and specific window capture with DPI awareness.

Features:
- Full screen capture using BitBlt
- Specific window capture using PrintWindow
- High DPI support for modern displays
- Multiple output formats (BMP, PNG, JPG)
- Continuous capture with configurable intervals
- Optional callback function for custom processing

Usage:
    # Capture full screen every 2 seconds for 20 seconds
    capture = ContinuousCapture()
    capture.continuous_capture(interval=2, duration=20, pformat="png")

Requirements:
    - Windows OS
    - pywin32 package
    - PIL/Pillow package

Author: Moli Studio
Modified by: geezmolycos
"""

import os
import time

isWindows = True if os.name == "nt" else False

if isWindows:
    from ctypes import windll
    from PIL import Image

    import win32con
    import win32gui
    import win32ui

    # Enable high DPI scaling for high-resolution displays
    # 0: No scaling, 1: All screens, 2: Current screen
    try:  # >= Windows 8.1
        windll.shcore.SetProcessDpiAwareness(1)
    except:  # Windows 8.0 or older
        try:
            windll.user32.SetProcessDPIAware()
        except:
            pass
    try:
        system_dpi = windll.user32.GetDpiForSystem()
    except:
        system_dpi = 96.0


class ContinuousCapture:
    def __init__(self, hwnd=None):
        """
        Initialize continuous capture utility

        Args:
            hwnd: Window handle to capture. If None, captures the entire screen.
        """
        # Print mode: 0b10 includes title/toolbar, 0b11 excludes them
        self.print_mode = 0b11
        
        # If no hwnd provided, use desktop window for full screen capture
        if hwnd is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = hwnd

        # Get window dimensions
        self.width, self.height = self.getRect()
        self.dpi_width, self.dpi_height = self.width, self.height

        # Device context and bitmap objects (initialized in setup_resources)
        self.hwndDC = None
        self.mfcDC = None
        self.saveDC = None
        self.saveBitMap = None

        # Initialize resources
        self.setup_resources()

    def set_hwnd(self, hwnd):
        if self.hwnd != hwnd:
            self.cleanup_resources()
            self.hwnd = hwnd
            self.width, self.height = self.getRect()
            self.setup_resources()

    def setup_resources(self):
        """Initialize resources needed for screenshot capture"""
        self.dpi_width, self.dpi_height = self.getDpiRect()

        # Get window device context
        self.hwndDC = win32gui.GetWindowDC(self.hwnd)
        self.mfcDC = win32ui.CreateDCFromHandle(self.hwndDC)
        self.saveDC = self.mfcDC.CreateCompatibleDC()

        # Create bitmap object
        self.saveBitMap = win32ui.CreateBitmap()
        self.saveBitMap.CreateCompatibleBitmap(self.mfcDC, self.dpi_width, self.dpi_height)

        # Select bitmap into device context
        self.saveDC.SelectObject(self.saveBitMap)

    def getRect(self):
        if not self.hwnd:
            return 0, 0
        if self.print_mode == 0b10:
            # 0b10: Get window position and size, including title bar and toolbar
            get_rect = win32gui.GetWindowRect(self.hwnd)
        else:
            # 0b11: Get window size, excluding title bar and toolbar
            get_rect = win32gui.GetClientRect(self.hwnd)
        width = get_rect[2] - get_rect[0]
        height = get_rect[3] - get_rect[1]
        return width, height

    def getDpiRect(self):
        """Get actual window size based on DPI scaling"""
        if self.hwnd == win32gui.GetDesktopWindow():
            try:
                hdc = win32gui.GetDC(self.hwnd)
                app_width = win32ui.GetDeviceCaps(hdc, win32con.HORZRES)
                sys_width = win32ui.GetDeviceCaps(hdc, win32con.DESKTOPHORZRES)
                dpi = sys_width / app_width
            except:
                dpi = 1.0
            finally:
                win32gui.ReleaseDC(self.hwnd, hdc)
        else:
            app_dpi = windll.user32.GetDpiForWindow(self.hwnd)
            dpi = app_dpi / system_dpi
        return int(self.width * dpi), int(self.height * dpi)

    @staticmethod
    def find_window_by_title(window_title):
        """
        Find window handle by window title

        Args:
            window_title: Window title (can be partial match)

        Returns:
            Window handle, or None if not found
        """

        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd) and window_title in win32gui.GetWindowText(hwnd):
                hwnds.append(hwnd)
                return False  # Stop enumeration, only need to find one
            return True

        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        return hwnds[0] if hwnds else None

    def capture_window(self):
        """
        Capture a single window

        Returns:
            Tuple of (bitmap data, width, height)
        """
        # Check if window size changed
        new_width, new_height = self.getRect()

        # If window size changed, reinitialize resources
        if new_width != self.width or new_height != self.height:
            self.cleanup_resources()
            self.width = new_width
            self.height = new_height
            self.setup_resources()

        # Use PrintWindow instead of BitBlt to solve black screen issues for background windows
        # Note: PrintWindow cannot capture desktop
        windll.user32.PrintWindow(self.hwnd, self.saveDC.GetSafeHdc(), self.print_mode)

        # Get bitmap information
        bmpinfo = self.saveBitMap.GetInfo()
        bmpstr = self.saveBitMap.GetBitmapBits(True)

        return bmpstr, bmpinfo['bmWidth'], bmpinfo['bmHeight']

    def capture_screen(self):
        """
        Capture the entire screen

        Returns:
            Tuple of (bitmap data, width, height)
        """
        # Check if window size changed
        new_width, new_height = self.getRect()

        # If window size changed, reinitialize resources
        if new_width != self.width or new_height != self.height:
            self.cleanup_resources()
            self.width = new_width
            self.height = new_height
            self.setup_resources()

        # PrintWindow cannot capture desktop, must use BitBlt
        # Note: BitBlt may show black for background windows
        try:
            # Save bitmap to memory device context
            self.saveDC.BitBlt((0, 0), (self.dpi_width, self.dpi_height), self.mfcDC, (0, 0), win32con.SRCCOPY)
        except:
            pass

        # Get bitmap information
        bmpinfo = self.saveBitMap.GetInfo()
        bmpstr = self.saveBitMap.GetBitmapBits(True)

        return bmpstr, bmpinfo['bmWidth'], bmpinfo['bmHeight']

    def cleanup_resources(self):
        """Clean up resources"""
        try:
            if self.saveBitMap:
                win32gui.DeleteObject(self.saveBitMap.GetHandle())
                self.saveBitMap = None

            if self.saveDC:
                self.saveDC.DeleteDC()
                self.saveDC = None

            if self.mfcDC:
                self.mfcDC.DeleteDC()
                self.mfcDC = None

            if self.hwndDC:
                win32gui.ReleaseDC(self.hwnd, self.hwndDC)
                self.hwndDC = None
        except:
            pass

    def capture_to_file(self, save_path):
        """
        Capture screenshot and save to file

        Args:
            save_path: Path to save the screenshot
        """
        self.capture_screen()
        # Save bitmap to file
        self.saveBitMap.SaveBitmapFile(self.saveDC, save_path)

    def capture_to_pil(self):
        """
        Capture screenshot and return as PIL Image

        Returns:
            PIL Image object
        """
        bmpstr, width, height = self.capture_screen()
        
        # Convert bitmap to PIL Image
        img = Image.frombuffer(
            'RGB',
            (width, height),
            bmpstr, 'raw', 'BGRX', 0, 1
        )
        
        return img

    def continuous_capture(self, interval=1, duration=10, output_dir="screenshots",
                           pformat="bmp", callback=None):
        """
        Continuous screenshot capture function

        Args:
            interval: Screenshot interval in seconds
            duration: Total duration in seconds
            output_dir: Output directory path
            pformat: Image format ("bmp", "png", or "jpg")
            callback: Optional callback function receiving (image_path, PIL_image)
        """
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Calculate number of screenshots
        num_shots = int(duration / interval)

        print(f"Starting continuous capture: {num_shots} screenshots, {interval} second intervals")

        for i in range(num_shots):
            # Generate filename
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}_{i + 1:04d}.{pformat}"
            save_path = os.path.join(output_dir, filename)

            # Execute screenshot
            if pformat == "bmp":
                self.capture_to_file(save_path)
                pil_img = None
            else:
                pil_img = self.capture_to_pil()
                pil_img.save(save_path)

            print(f"Saved screenshot: {save_path}")

            # Call callback function if provided
            if callback:
                callback(save_path, pil_img)

            # Wait for next screenshot (skip waiting on last iteration)
            if i < num_shots - 1:
                time.sleep(interval)

        print("Capture complete")

    def __del__(self):
        """Destructor to ensure resources are properly released"""
        self.cleanup_resources()


# Usage examples
if __name__ == "__main__":
    # Example 1: Capture entire screen every 2 seconds for 20 seconds, save as PNG
    capture = ContinuousCapture()
    capture.continuous_capture(
        interval=2,
        duration=20,
        output_dir="screen_shots",
        pformat="png"
    )

    # Example 2: Capture specific window (e.g., Notepad) every 1 second for 10 seconds
    # hwnd = ContinuousCapture.find_window_by_title("Notepad")
    # if hwnd:
    #     capture = ContinuousCapture(hwnd=hwnd)
    #     capture.continuous_capture(
    #         interval=1,
    #         duration=10,
    #         output_dir="notepad_shots"
    #     )
    # else:
    #     print("Window not found")

    # Example 3: Using callback function to process screenshots
    # def process_image(path, img):
    #     if img:  # If not BMP format, img will be a PIL Image object
    #         # Process image here, e.g., resize, add watermark, etc.
    #         small_img = img.resize((img.width // 2, img.height // 2))
    #         small_img.save(path.replace('.png', '_small.png'))
    #
    # capture = ContinuousCapture()
    # capture.continuous_capture(
    #     interval=1,
    #     duration=5,
    #     output_dir="processed_shots",
    #     pformat="png",
    #     callback=process_image
    # )
