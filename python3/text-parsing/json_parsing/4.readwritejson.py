import json

with open('input.json') as IF:
    jsonData = json.load(IF)
    print('Input JSON file\n{}'.format(jsonData))

    jsonData['name'] = 'John'
    jsonData['reportees'][0]['name'] = 'Jamie'
    jsonData['reportees'][0]['age'] = '38'
    jsonData['reportees'][0]['reportees'] = [{'name': 'Cal', 'age': 29, 'reportees': None}]
    jsonData['reportees'][1]['name'] = 'Adam'
    jsonData['reportees'][1]['age'] = '40'
    jsonData['reportees'][1]['reportees'] = [{'name': 'Smith', 'age': 27, 'reportees': None}]

with open('results.json', 'w') as OF:
    json.dump(jsonData, OF)  # Writing data to JSON file

print('\nOutput JSON file with modifications')
with open('results.json', 'r') as IF:
    print(IF.read())
