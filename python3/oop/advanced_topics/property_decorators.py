class Employee:
    def __init__(self, first, last):
        self.first = first
        self.last = last

    @property
    def email(self):
        return "{}.{}@email.com".format(self.first, self.last)

    @property
    def fullname(self):
        return "{} {}".format(self.first, self.last)

    @fullname.setter
    def fullname(self, name):
        fname, lname = name.split(' ')
        self.first = fname
        self.last = lname


emp1 = Employee('Sid', 'Sharma')
print(emp1.fullname)
emp1.fullname = 'Vibhu Kaul'
print(emp1.email)
