```markdown
# Практическое задание 5: Регулярные выражения Python (RegEx)

## О проекте
Этот проект содержит решения для практического задания по регулярным выражениям в Python. Здесь два основных задания: парсинг чека и упражнения по RegEx.

## Структура проекта
```
Practice5/
│
├── receipt_parser.py    # Парсер чека (работа с raw.txt)
├── raw.txt              # Файл с чеком из аптеки
├── regex.md             # Упражнения по регулярным выражениям
└── README.md            # Этот файл
```

## Задание 1: Парсинг чека
1. Извлечь все цены
2. Найти все названия товаров
3. Рассчитать общую сумму
4. Извлечь дату и время
5. Найти способ оплаты
6. Создать структурированный вывод (JSON)

## Задание 2: Упражнения по RegEx
1. a followed by zero or more b's
2. a followed by two to three b
3. lowercase letters joined with underscore
4. one uppercase followed by lowercase
5. a followed by anything ending in b
6. replace space, comma, dot with colon
7. snake case to camel case
8. split at uppercase letters
9. insert spaces between capital letters
10. camel case to snake case

## Как запустить
```bash
# Запуск парсера чека
python receipt_parser.py

# Запуск упражнений по RegEx
python regex_solutions.py
```

## Используемые regex

### В парсере чека:
- Поиск цен: `\d+[,\d\s]+\.?\d*`
- Поиск товаров: `\d+\.\s*(.*?)\s*\d+[,\d]*\s*x`
- Поиск даты: `Время:\s*([\d.]+ [\d:]+)`
- Поиск итога: `ИТОГО:\s*([\d\s,]+)`

### В упражнениях:
- `ab*` - a и ноль или больше b
- `ab{2,3}` - a и ровно 2-3 b
- `[a-z]+_[a-z]+` - маленькие буквы + _ + маленькие буквы
- `[A-Z][a-z]+` - большая буква + маленькие
- `^a.*b$` - начинается на a, заканчивается на b
- `[ ,.]` - пробел, запятая или точка
- `(?<!^)(?=[A-Z])` - вставка перед большой буквой