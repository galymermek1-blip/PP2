import re

# 1
# Найти строки, где после 'a' идет ноль или больше 'b'
print("1")
print("---")

def proverka1(text):
    if re.fullmatch(r'ab*', text):
        return True
    return False

slova = ['a', 'ab', 'abb', 'abbb', 'b', 'abc', 'abbbbc']

for slovo in slova:
    if proverka1(slovo):
        print(f"{slovo} - да")
    else:
        print(f"{slovo} - нет")


# 2
# Найти строки, где после 'a' идет 2 или 3 буквы 'b'
print("\n2")
print("---")

def proverka2(text):
    if re.fullmatch(r'ab{2,3}', text):
        return True
    return False

slova = ['ab', 'abb', 'abbb', 'abbbb', 'a', 'abc']

for slovo in slova:
    if proverka2(slovo):
        print(f"{slovo} - да")
    else:
        print(f"{slovo} - нет")


# 3
# Найти слова из маленьких букв, соединенных подчеркиванием
print("\n3")
print("---")

text = "hello_world test_example python_programming HELLO_WORLD privet_kak_dela"
naideno = re.findall(r'[a-z]+_[a-z]+', text)

print(f"Текст: {text}")
print(f"Найдено: {naideno}")


# 4
# Найти слова, которые начинаются с большой буквы, а дальше маленькие
print("\n4")
print("---")

text = "Hello World Python JAVA JavaScript Privet KakDela"
naideno = re.findall(r'[A-Z][a-z]+', text)

print(f"Текст: {text}")
print(f"Найдено: {naideno}")


# 5
# Найти строки, которые начинаются с 'a' и заканчиваются на 'b'
print("\n5")
print("---")

def proverka5(text):
    if re.match(r'^a.*b$', text):
        return True
    return False

slova = ['ab', 'acb', 'a123b', 'a!@#b', 'a b', 'abc', 'ba']

for slovo in slova:
    if proverka5(slovo):
        print(f"{slovo} - да")
    else:
        print(f"{slovo} - нет")


# 6
# Заменить пробелы, запятые и точки на двоеточие
print("\n6")
print("---")

text = "Привет, мир. Это тест, с пробелами и точками."
result = re.sub(r'[ ,.]', ':', text)

print(f"Было: {text}")
print(f"Стало: {result}")


# 7
# Перевести из snake_case в camelCase
print("\n7")
print("---")

def snake_to_camel(text):
    slova = text.split('_')
    result = slova[0]
    for slovo in slova[1:]:
        result += slovo.capitalize()
    return result

primery = ['hello_world', 'python_programming', 'mama_myla_ramu']

for primer in primery:
    camel = snake_to_camel(primer)
    print(f"{primer} -> {camel}")


# 8
# Разбить строку по большим буквам
print("\n8")
print("---")

text = "HelloWorldPythonProgramming"
slova = re.findall(r'[A-Z][a-z]*', text)

print(f"Было: {text}")
print(f"Стало: {slova}")


# 9
# Вставить пробелы перед большими буквами
print("\n9")
print("---")

def vstavit_probeli(text):
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', text)

primery = ['HelloWorld', 'PythonProgramming', 'CamelCaseExample']

for primer in primery:
    result = vstavit_probeli(primer)
    print(f"{primer} -> {result}")


# 10
# Перевести из camelCase в snake_case
print("\n10")
print("---")

def camel_to_snake(text):
    s_podcherk = re.sub(r'(?<!^)(?=[A-Z])', '_', text)
    return s_podcherk.lower()

primery = ['helloWorld', 'pythonProgramming', 'camelCaseExample']

for primer in primery:
    result = camel_to_snake(primer)
    print(f"{primer} -> {result}")