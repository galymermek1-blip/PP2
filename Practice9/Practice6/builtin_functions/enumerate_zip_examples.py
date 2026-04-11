names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 78]

print("Using enumerate():")
for index, name in enumerate(names, start=1):
    print(index, name)

print("\nUsing zip():")
for name, score in zip(names, scores):
    print(name, score)