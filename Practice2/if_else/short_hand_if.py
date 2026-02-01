# short_hand_if.py
# Example 1: One-line if statement
a = 5
b = 2
if a > b: print("a is greater than b")

# Example 2: Ternary operator
a = 2
b = 330
print("A") if a > b else print("B")

# Example 3: Value assignment with ternary
a = 10
b = 20
bigger = a if a > b else b
print("Bigger is", bigger)

# Example 4: Logical AND operator
a = 200
b = 33
c = 500
if a > b and c > a:
    print("Both conditions are True")

# Example 5: Logical OR operator
a = 200
b = 33
c = 500
if a > b or a > c:
    print("At least one of the conditions is True")
