# filter() selects elements
numbers = [10, 15, 20, 25, 30]

greater_than_20 = list(filter(lambda x: x > 20, numbers))

print("Numbers > 20:", greater_than_20)
