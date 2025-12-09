import os, sys

def resource_path(relative_path: str) -> str:
    """
    Resolve resource paths for both dev and PyInstaller exe.
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
