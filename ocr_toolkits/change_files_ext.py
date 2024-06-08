
import os
import shutil

def change_files_ext(src_dir, dst_dir, new_ext):
    """
    Change the extension of all files in src_dir and move them to dst_dir.

    Parameters:
    src_dir (str): The source directory containing the files.
    dst_dir (str): The destination directory where the files will be moved.
    new_ext (str): The new file extension (e.g., '.png').
    """
    # Ensure the destination directory exists
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # Iterate over all files in the source directory
    for filename in os.listdir(src_dir):
        # Only process files (ignore directories)
        if os.path.isfile(os.path.join(src_dir, filename)):
            # Get the file name without the extension
            base = os.path.splitext(filename)[0]
            # Construct the new file name with the new extension
            new_filename = base + new_ext
            # Move the file to the destination directory with the new extension
            shutil.move(os.path.join(src_dir, filename), os.path.join(dst_dir, new_filename))

