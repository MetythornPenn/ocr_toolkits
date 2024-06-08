import os
from typing import Optional

def delete_files_ext(dir: str, ext: Optional[str] = None) -> None:
    try:
        for filename in os.listdir(dir):
            file_path = os.path.join(dir, filename)
            if os.path.isfile(file_path):
                if ext is None or filename.endswith(ext):
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")