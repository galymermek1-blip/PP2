import shutil
import os

source_file = "sample.txt"
backup_file = "sample_backup.txt"

if os.path.exists(source_file):
    shutil.copy(source_file, backup_file)
    print(f"Copied {source_file} to {backup_file}")
else:
    print(f"{source_file} does not exist")

file_to_delete = "sample_backup.txt"

if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print(f"Deleted {file_to_delete} safely")
else:
    print(f"{file_to_delete} not found")