class Employee:
    num_of_emps = 0  # Class variable

    def __init__(self, first, last, salary):
        self.first = first
        self.last = last
        self.salary = salary
        Employee.num_of_emps += 1

    def __del__(self):
        Employee.num_of_emps -= 1

    def details(self):
        print("{} {} has {} salary".format(self.first, self.last, self.salary))


if __name__ == "__main__":
    print(Employee.num_of_emps)
    emp1 = Employee('Johny', 'Cash', 5000)
    print(Employee.num_of_emps)
    emp2 = Employee('Tommy', 'Lee', 8000)
    print(Employee.num_of_emps)
    emp3 = Employee('', '', '')
    print(Employee.num_of_emps)
    del emp1
    print(Employee.num_of_emps)
    del emp2
    print(Employee.num_of_emps)
    del emp3
    print(Employee.num_of_emps)
