class Animal:
    def sound(self):
        print("sound")


class Dog(Animal):
    def sound(self):
        print("Dog barks")


dog = Dog()
dog.sound()
