def deco(f=None, /, *, repeat=3):
    """This is a parameterized decorator but using a single outer function
    A traditional parameterized decorator looks like this which requires 2 nested functions
    
    def outer_func(*args, **kwargs):
        def decorator(func):
            def inner(*a, **kw):
                # do some stuff before calling f
                res = f()
                # do some stuff after calling f
            return inner
        return decorator
    
    This version uses functools.partial & avoids defining one extra nested function
    
    Another peculiar aspect is that you can call use decorator with/without parens
    @deco
    def some_func():
        ...
    
    @deco(repeat=10)
    def some_func():
    ...
    
    Try decorating a function with a regular parameterized decorator without parenthesis, and it will fail with 
    a TypeError - missing 1 required positional argument:
    
    """
    @wraps(f)
    def inner(*a, **kw):
        print(f"Before calling {f.__name__}")
        print(f"Value of repeat is {repeat}")
        res = f(*a, **kw) * repeat
        print(f"Result of calling {f.__name__} is {res}")
        print(f"After calling {f.__name__}")
    
    if f is None:    
        # decorator was called with parenthesis by passing the keyword args
        # so we need to return a partial function by setting the provided kwargs, 
        # so that python can call by it passing the fxn being decorated 
        return partial(deco, repeat=repeat)
    # decorator was called without parenthesis, which means python already provided the 
    # fxn being decorated here, so we simply need to return the inner function
    return inner
  
  
  
  # Usage
  @deco
def greet(name):
    return f"Hi {name} !"
    
# greet("Rohit")
# Before calling greet
# Value of repeat is 3
# Result of calling greet is Hi Rohit !Hi Rohit !Hi Rohit !
# After calling greet

@deco(repeat=5)
def greet(name):
    return f"Hi {name} !"
    
# greet("Rohit")
# Before calling greet
# Value of repeat is 5
# Result of calling greet is Hi Rohit !Hi Rohit !Hi Rohit !Hi Rohit !Hi Rohit !
# After calling greet
