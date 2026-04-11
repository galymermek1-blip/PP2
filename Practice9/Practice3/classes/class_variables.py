class Student:
    school = "ABC School"  # class variable

    def __init__(self, name):
        self.name = name    # instance variable


s1 = Student("Ali")
s2 = Student("Sara")

print(s1.school)
print(s2.school)

Student.school = "XYZ School"  # change class variable

print(s1.school)
print(s2.school)
