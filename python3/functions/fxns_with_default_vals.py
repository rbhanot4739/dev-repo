# Never pass a mutable object as default value to a kwarg
# to see the bad effect run this fxn multiple time


def mutable_default_vals(val, x=0, li=[]):
    li.extend(val)
    x = x + 5
    print(x, li)


mutable_default_vals([10, 20])
mutable_default_vals([10, 20])
mutable_default_vals([10, 20])
mutable_default_vals([10, 20])
