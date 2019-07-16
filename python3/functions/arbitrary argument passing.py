# for passing arbitrary number of arguments to the fxn we have to use asterix operator in front of param name.. this will make a tuple of params.
def avg(*val):
    sum = 0
    for i in val:
        sum += i
    print(sum)


def locations(city, *others_cities):
    print(city, others_cities)


def argtest(*attr, **val):
    print(attr, val)


# avg(1,2,3,4,5)
# avg(10,20)
# list1=[10,20,30,40]
# avg(*list1) # for passing a string/list/tuple we have to append asterix before the list in fxn calling
#
#
# locations('Delhi')
# locations('Noida', 'Mumbai', 'Kolkota')


argtest("name", "city", "comp", name="rohit", city="noida", comp="ericsson")
