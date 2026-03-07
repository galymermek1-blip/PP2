from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

squared = list(map(lambda x: x * x, numbers))
print("Squared numbers:", squared)

even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", even_numbers)

total = reduce(lambda x, y: x + y, numbers)
print("Sum of numbers:", total)

value = "123"
converted_value = int(value)

print("Type of value:", type(value))
print("Type after conversion:", type(converted_value))