# https://realpython.com/blog/python/instance-class-and-static-methods-demystified/


class Name:
    def __init__(self, fname, lname, age):
        self.fname = fname
        self.lname = lname
        self.age = age

    def details(self):
        print('{} {} is {} years old'.format(self.fname, self.lname, self.age))

    @classmethod
    def name_frm_str(cls, name_str):
        fname, lname, age = name_str.split('/')
        return cls(fname, lname, age)


obj1 = Name('John', 'Smith', 25)
obj1.details()

obj2 = Name.name_frm_str('Tom/Hardy/37')
obj2.details()
print(obj2.fname)
