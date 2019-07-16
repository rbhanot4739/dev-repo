import json

# with open(r'C:\Users\erotbht\Documents\Study\Python\Python_my_Scripts\Data\grades.json', "r", encoding="utf8") as inputJson:
with open(r'C:\Users\erotbht\Documents\Study\Perl\Documentation\Scripts\params.json', "r",
          encoding="utf8") as inputJson:
    pydata = json.load(inputJson)
    for k in pydata:
        print(k, " = ", pydata[k])
