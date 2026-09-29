from abc import ABC, abstractmethod
# Abstrct Base Class
class Calculator(ABC):
    @abstractmethod
    def add(self,a,b):
        pass
    @abstractmethod
    def subtract(self,a,b):
        pass

    def mul(self,a,b):
        pass




class simpleclac(Calculator):
    def add(self,a,b):
        return (a+b)

    def mul(self, a, b):
        return (a *  b)

    def subtract(self, a, b):
        return (a- b)


calc = simpleclac()
print(calc.add(5,10))
print(calc.subtract(5,10))
print(calc.mul(5,10))

