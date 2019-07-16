from collections import defaultdict


def dget():
    data = 'ggegrjehubnhbdhbrhbvhbsjdfytbsLlsljfdydbrfsjgeegfdvfrsh'
    data2 = 'AJYGHBJNSMBjkjhebwehvegvwghwyueiojkdnfvdbnm'
    normal_dict = {}
    # Using normal dictionaries
    for char in data:
        if char in normal_dict:
            normal_dict[char] += 1
        else:
            normal_dict[char] = 1

    for char in data2:
        print(char, ' -->', normal_dict.get(char, "Key doesn't exist"))


def defaultdicttest():
    """ Demonstration of how to use default dicts """
    int_dict = defaultdict(int)
    data = 'ggegrjehubnhbdhbrhbvhbsjdfytbsLlsljfdydbrfsjgeegfdvfrsh'

    for char in data:
        # Using default dicts
        int_dict[char] += 1
    return int_dict


print(defaultdicttest())
print(dget())
