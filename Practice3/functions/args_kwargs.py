def sum_all(*numbers):
    """Sum any number of values."""
    total = 0
    for n in numbers:
        total += n
    print("Sum:", total)


def show_profile(**info):
    """Display user profile information."""
    for key, value in info.items():
        print(key, ":", value)


sum_all(1, 2, 3, 4)
show_profile(name="Ali", age=20, country="Kazakhstan")
