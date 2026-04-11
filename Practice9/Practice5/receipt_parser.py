import re, json

text = open('raw.txt', encoding='utf-8').read()

print("ПАРСИНГ ЧЕКА\n" + "="*30)

# 1. Extract all prices from the receipt
# Нужно найти все цены в чеке (числа с запятыми и пробелами)
print("\n1. Все цены")
ceny = re.findall(r'\d+[,\d\s]+\.?\d*', text)
print(f"Найдено: {len(ceny)}", ceny[:3])

# 2. Find all product names
# Нужно найти названия всех товаров (идут после номера и до количества)
print("\n2. Названия товаров")
tovary = re.findall(r'\d+\.\s*(.*?)\s*\d+[,\d]*\s*x', text, re.DOTALL)
tovary = [re.sub(r'\s+', ' ', t).replace('[RX]-', '').strip() for t in tovary]
print(f"Найдено: {len(tovary)}", [t[:20]+'...' for t in tovary[:3]])

# 3. Calculate total amount
# Нужно найти итоговую сумму в чеке
print("\n3. Общая сумма")
itogo = re.search(r'ИТОГО:\s*([\d\s,]+)', text)
summa = float(itogo.group(1).replace(',', '').replace(' ', '')) if itogo else 0
print(f"ИТОГО: {summa} тенге")

# 4. Extract date and time information
# Нужно найти дату и время покупки
print("\n4. Дата и время")
data = re.search(r'Время:\s*([\d.]+ [\d:]+)', text)
print(data.group(1) if data else "Не найдено")

# 5. Find payment method
# Нужно определить чем оплатили (карта или наличные)
print("\n5. Способ оплаты")
oplata = 'Банковская карта' if 'Банковская карта' in text else 'Наличные'
print(oplata)

# 6. Create a structured output (JSON or formatted text)
# Нужно собрать все данные в структурированном виде (JSON)
print("\n6. JSON")
result = {
    "цены": ceny[:5],
    "товары": tovary[:3],
    "сумма": summa,
    "дата": data.group(1) if data else None,
    "оплата": oplata
}
print(json.dumps(result, ensure_ascii=False, indent=2))