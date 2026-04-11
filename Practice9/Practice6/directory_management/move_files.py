import shutil
import os

source_folder = "source_dir"
destination_folder = "destination_dir"

os.makedirs(source_folder, exist_ok=True)
os.makedirs(destination_folder, exist_ok=True)

test_file = os.path.join(source_folder, "example.txt")

with open(test_file, "w", encoding="utf-8") as file:
    file.write("This file will be moved and copied.\n")

copied_file = os.path.join(destination_folder, "example_copy.txt")
shutil.copy(test_file, copied_file)
print("File copied successfully")

moved_file = os.path.join(destination_folder, "example_moved.txt")
shutil.move(test_file, moved_file)
print("File moved successfully")