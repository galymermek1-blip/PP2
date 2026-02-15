class Person:
    def __init__(self, name):
        self.name = name


class Student(Person):
    def __init__(self, name, grade):
        super().__init__(name)  # call parent constructor
        self.grade = grade


s = Student("Ali", "A")
print(s.name, s.grade)
