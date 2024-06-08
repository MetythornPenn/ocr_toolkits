import os
import shutil
from typing import Optional

def move_files_ext(src_dir: str, dst_dir: str, ext: Optional[str] = None) -> None:
    try:
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)

        for filename in os.listdir(src_dir):
            src_file_path = os.path.join(src_dir, filename)
            if os.path.isfile(src_file_path):
                if ext is None or filename.endswith(ext):
                    dst_file_path = os.path.join(dst_dir, filename)
                    shutil.move(src_file_path, dst_file_path)
                    print(f"Moved file: {src_file_path} -> {dst_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
