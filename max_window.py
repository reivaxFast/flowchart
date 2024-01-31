import win32con
import win32gui
#win32con and win32gui in pywin32 e.g. pip install pywin32
class Call_Window():
    def __init__():
        pass

    def find_window(window_title):
        # Use window title to get window's handle
        window_handle = win32gui.FindWindow(None,window_title)
        return window_handle

    def maximize_window(window_handle):
            # Get current status
            window_placement = win32gui.GetWindowPlacement(window_handle)
            
            # If minimized currently, restore it
            if window_placement[1] == win32con.SW_SHOWMINIMIZED:
                win32gui.ShowWindow(window_handle, win32con.SW_RESTORE)
            
            # Maximize it
            win32gui.ShowWindow(window_handle, win32con.SW_MAXIMIZE)