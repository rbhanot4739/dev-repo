import requests

url = 'http://www.pixelstalk.net/wp-content/uploads/2016/07/3D-nature-landscape-photo-of-mountaint.jpg'

req = requests.get(url)

try:
    req.raise_for_status()
    with open('Forest.jpg', 'wb') as OF:
        for chunk in req.iter_content(chunk_size=50000):
            OF.write(chunk)
except Exception as e:
    print(e)

print('done')
