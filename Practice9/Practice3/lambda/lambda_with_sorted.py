# sorted() with custom rule
students = [
    ("Ali", 85),
    ("Sara", 92),
    ("John", 78)
]

sorted_by_score = sorted(students, key=lambda student: student[1])

print("Sorted by score:", sorted_by_score)
