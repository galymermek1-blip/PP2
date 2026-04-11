class Father:
    def skills(self):
        print("Driving")


class Mother:
    def skills(self):
        print("Cooking")


class Child(Father, Mother):
    pass


c = Child()
c.skills()  # method from Father is used first
