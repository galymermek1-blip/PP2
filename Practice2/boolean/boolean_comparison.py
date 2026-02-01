# boolean_comparison.py
# Example 1: Comparison operators
print(10 > 9)
print(10 == 9)
print(10 < 9)

# Example 2: If statement with comparison
a = 200
b = 33
if b > a:
    print("b is greater than a")
else:
    print("b is not greater than a")

# Example 3: Custom class with __len__
class myclass():
    def __len__(self):
        return 0

myobj = myclass()
print(bool(myobj))

# Example 4: isinstance() function
x = 200
print(isinstance(x, int))
