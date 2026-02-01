# for_continue.py
# Example 1: Continue to skip element
fruits = ["apple", "banana", "cherry"]
for x in fruits:
    if x == "banana":
        continue
    print(x)

# Example 2: For with else clause
for x in range(6):
    print(x)
else:
    print("Finally finished!")

# Example 3: Nested loops
adj = ["red", "big", "tasty"]
fruits = ["apple", "banana", "cherry"]
for x in adj:
    for y in fruits:
        print(x, y)

# Example 4: Pass statement
for x in [0, 1, 2]:
    pass
