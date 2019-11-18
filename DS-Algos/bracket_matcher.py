def bracket_matcher(data):
    count = 0
    for i in data:
        if i in ('{', '[', '('):
            count += 1
        elif i in ('}', ']', ')'):
            count -= 1
        if count < 0:
            return False
    return count == 0


inp = '[]'

if bracket_matcher(inp):
    print("Matched")
else:
    print("Failed")
