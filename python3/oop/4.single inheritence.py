class Employee:
    raise_amount = 1.1

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = (self.first).lower() + '.' + (self.last).lower() + '@email.com'

    def __repr__(self):
        return "{}({},{},{})".format(type(self).__name__, self.first, self.last, self.pay)

    def __str__(self):
        return "{} : {} {}".format(type(self).__name__, self.first, self.last)

    def pay_raise(self):
        return int(self.pay * type(self).raise_amount)


class Developers(Employee):
    raise_amount = 1.3

    def __init__(self, first, last, pay, lang):
        super().__init__(first, last, pay)
        self.lang = lang

    def __str__(self):
        return '{}, {}'.format(super().__str__(), self.lang)


class Devops(Developers):
    raise_amount = 1.6

    def __init__(self, first, last, pay, lang, admin):
        super().__init__(first, last, pay, lang)
        self.admin = admin

    def __str__(self):
        return "{}, {}".format(super().__str__(), self.admin)


class Manager(Employee):
    raise_amount = 1.7

    def __init__(self, first, last, pay, reportees=None):
        super().__init__(first, last, pay)
        if reportees is None:
            self.reportees = []
        else:
            self.reportees = reportees

    def __str__(self):
        return '{} --> {}'.format(super().__str__(), self.reportees)

    def add_reportee(self, reportee):
        if reportee not in self.reportees:
            self.reportees.append(reportee)

    def remove_reportee(self, reportee):
        if reportee in self.reportees:
            self.reportees.remove(reportee)


if __name__ == "__main__":
    emp1 = Employee('Sid', 'K', 50000)

    dvp1 = Developers('Sid', 'K', 50000, 'C++')
    dvp2 = Developers('R', 'B', 50000, 'Python')
    dvp3 = Developers('R', 'J', 50000, 'Perl')

    dev1 = Devops('Robin', 'Smith', 80000, 'Python', 'Linux')
    # print(dev1.fullname(),dev1.admin,dev1.lang,dev1.pay,dev1.pay_raise())
    # print(dev1)

    mgr1 = Manager('P', 'Q', 150000, [dvp1, dvp3, dev1])
    mgr1.add_reportee(dvp2)
    mgr1.remove_reportee(dvp1)
    # mgr1.print_reportees()
    # print(mgr1)  # print(repr(mgr1))
    print(Developers.__mro__)
