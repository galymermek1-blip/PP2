# 1. Generator that generates squares up to n
def square_generator(n):
    for i in range(n + 1):
        yield i * i

# 2. Print even numbers between 0 and n in comma separated form
def even_numbers(n):
    for i in range(0, n + 1, 2):
        yield i

# 3. Generator for numbers divisible by 3 and 4 between 0 and n
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

# 4. Generator squares from a to b
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i

# 5. Generator returns all numbers from n down to 0
def countdown(n):
    while n >= 0:
        yield n
        n -= 1
    