from pathlib import Path
import sys

def get_folder(Target = None):
    if getattr(sys, 'frozen', False):
        # If running from a bundled executable (e.g., PyInstaller)
        base_path = Path(sys._MEIPASS)
    else:
        # If running from source
        base_path = Path(__file__).resolve().parent.parent.parent

    return base_path / Target if Target else base_path
