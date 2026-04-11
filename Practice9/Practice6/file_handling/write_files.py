with open("sample.txt", "a", encoding="utf-8") as file:
    file.write("This is a new added line.\n")
    file.write("Another appended line.\n")

with open("sample.txt", "r", encoding="utf-8") as file:
    content = file.read()

print("Updated file content:")
print(content)