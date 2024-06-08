import os
from typing import Optional

def rename_files_ext(
    src_dir: str, 
    start_num: int = 1, 
    prefix: Optional[str] = None,
    suffix: Optional[str] = None, 
    digit: int = 4, 
    ext: Optional[str] = None
) -> None:

    try:
        for index, filename in enumerate(os.listdir(src_dir), start=start_num):
            if ext is None or filename.endswith(ext):
                # Construct the new filename
                new_filename = f"{prefix if prefix else ''}{index:0{digit}d}{suffix if suffix else ''}"
                
                # Append the extension if it exists
                if ext and not filename.endswith(ext):
                    new_filename += ext
                
                src_file_path = os.path.join(src_dir, filename)
                dst_file_path = os.path.join(src_dir, new_filename)
                
                # Rename the file
                os.rename(src_file_path, dst_file_path)
                print(f"Renamed file: {src_file_path} -> {dst_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

