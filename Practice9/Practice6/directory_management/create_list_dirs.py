import os

nested_path = "test_folder/subfolder1/subfolder2"
os.makedirs(nested_path, exist_ok=True)
print("Nested directories created")

print("\nFiles and folders in current directory:")
for item in os.listdir("."):
    print(item)

print("\nPython files found:")
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py"):
            print(os.path.join(root, file))