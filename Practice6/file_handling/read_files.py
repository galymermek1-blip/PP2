with open("sample.txt", "w", encoding="utf-8") as file:
    file.write("Hello, this is the first line.\n")
    file.write("This is the second line.\n")
    file.write("Python file handling practice.\n")

with open("sample.txt", "r", encoding="utf-8") as file:
    content = file.read()

print("File content:")
print(content)