class Car:
    """Demonstration of class and instance variables"""
    engine = 'Petrol'

    def __init__(self, make, transmission, model):
        self.make = make
        self.transmission = transmission
        self.model = model

    def details(self):
        print('{}-{}, Engine: {}, Transmission: {}'.format(self.make, self.model, self.engine, self.transmission))


swift = Car('Suzuki', 'Manual', 'Swift')
swift.details()

innova = Car('Toyota', 'Manual', 'Innova')
innova.engine = 'Diesel'
innova.details()

baleno = Car('Suzuki', 'Automatic', 'Baleno')
baleno.details()
