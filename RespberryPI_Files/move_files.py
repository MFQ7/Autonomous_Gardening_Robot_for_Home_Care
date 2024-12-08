import os
import shutil

cur_run_dir = "/home/poison-ivy/Cur_Run"
prev_run_dir = "/home/poison-ivy/Prev_Run"
prev_run_subdir = os.path.join(prev_run_dir, "Prev_Run_1")

try:
    if not os.path.isdir(cur_run_dir):
        print(f"Directory '{cur_run_dir}' does not exist. Exiting.")
        exit(1)

    jpeg_files = [f for f in os.listdir(cur_run_dir) if f.endswith(".jpeg")]
    if not jpeg_files:
        print(f"No .jpeg files found in '{cur_run_dir}'. Exiting.")
        exit(1)
    os.makedirs(prev_run_subdir, exist_ok=True)

    for file_name in jpeg_files:
        source_path = os.path.join(cur_run_dir, file_name)
        dest_path = os.path.join(prev_run_subdir, file_name)
        shutil.move(source_path, dest_path)
        print(f"Moved: {file_name} -> {dest_path}")

    print(f"All .jpeg files moved to '{prev_run_subdir}'.")

except Exception as e:
    print(f"An error occurred: {e}")
