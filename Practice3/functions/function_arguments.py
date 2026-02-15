def introduce(name, age=18):
    """
    Introduce a person.
    age has a default value if not provided.
    """
    print("Name:", name)
    print("Age:", age)


introduce("Ali", 20)   # positional arguments
introduce("Sara")      # default value is used
