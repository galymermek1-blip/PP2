class Animal:
    def speak(self):
        print("Some sound")


class Cat(Animal):
    def speak(self):
        # overriding parent method
        print("Meow")


c = Cat()
c.speak()
