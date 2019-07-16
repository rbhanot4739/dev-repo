import pickle
from pprint import pprint

with open('searchresults.pkl', 'rb') as IF:
    res = pickle.load(IF)

# pprint(res.keys())
pprint(res['items'])
