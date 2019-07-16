class Car:
    def __init__(self, model, company, no_tyres):
        self.model = model
        self.company = company
        self.tyres = no_tyres

    @property
    def tyres(self):
        print("Getting value")
        return self._tyres

    @tyres.setter
    def tyres(self, value):
        if value > 2:
            print("Setting value")
            self._tyres = value
        else:
            print("Car atleast needs 3 tyres")

car1 = Car("Zen", "Maruti", 3)
car2 = Car("Zen", "Maruti", 9)
print(car1.tyres)
print(car2.tyres)
