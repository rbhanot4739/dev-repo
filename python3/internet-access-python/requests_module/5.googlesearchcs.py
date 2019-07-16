import pprint
from googleapiclient.discovery import build
import pickle


def search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    # pprint.pprint(res)
    with open('searchresults.pkl', 'wb') as of:
        pickle.dump(res, of)  # return res['items']


if __name__ == '__main__':
    api_key = 'AIzaSyCgz0--wXKFkmvYo8mjeBALpfuXS65AgKw'
    cse_id = '009928171693107249540:wrff2gtk0po'
    res = search('Nagios', api_key, cse_id)  # print(res)
