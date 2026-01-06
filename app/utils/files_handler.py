import shutil
from pathlib import Path

class FilesHandler:
    UPLOAD_DIR = Path("static/uploads")
    PROFILE_IMG_DIR = Path("static/profiles")
    
    @staticmethod
    def move_to_profile_image(filename: str) -> bool:
        source = FilesHandler.UPLOAD_DIR / filename
        target_dir = FilesHandler.PROFILE_IMG_DIR
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / filename
        if not source.exists():
            print(f"Error: {source} does not exist.")
            return False
        try:
            shutil.move(str(source), str(target))
        except Exception as e:
            print(f"Error moving file: {e}")
            return False
        return True
