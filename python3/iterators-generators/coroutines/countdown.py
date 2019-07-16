def countdown(pat):
    print('Started looking for ', pat)
    while True:
        data = (yield)
        if pat in data:
            print(pat, ' matched in ', data)

co = countdown('hon')
next(co)

for pat in ('ruby' , 'perl', 'python', 'cython', 'java', 'honor'):
    co.send(pat)