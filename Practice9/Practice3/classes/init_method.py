class Person:
    def __init__(self, name, age):
        # constructor initializes object data
        self.name = name
        self.age = age


p = Person("Ali", 20)
print(p.name, p.age)