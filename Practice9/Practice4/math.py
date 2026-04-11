import math

# 1. Convert degree to radian
degree = 15
radian = degree * (math.pi / 180)
print("Input degree:", degree)
print("Output radian:", radian)
print()

# 2. Calculate area of a trapezoid
height = 5
base1 = 5
base2 = 6
area_trapezoid = ((base1 + base2) / 2) * height
print("Height:", height)
print("Base, First value:", base1)
print("Base, second value:", base2)
print("Expected Output:", area_trapezoid)
print()

# 3. Calculate area of regular polygon
n = 4
side = 25
area_polygon = (n * side**2) / (4 * math.tan(math.pi / n))
print("Input number of sides:", n)
print("Input the length of a side:", side)
print("The area of the polygon is:", round(area_polygon))
print()

# 4. Calculate area of a parallelogram
base = 5
height_parallelogram = 6
area_parallelogram = base * height_parallelogram
print("Length of base:", base)
print("Height of parallelogram:", height_parallelogram)
print("Expected Output:", area_parallelogram)