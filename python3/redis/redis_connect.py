import redis

r = redis.Redis(host='127.0.0.1', port=6347,
                password='GKCfQWetSvAXtuBegdY8AMB72sAiyZx2f5Y2LfZwRsgEIvu74avAJQ3lp9LKaUgJys-GsrQuMy-wmDkY')


print('Fetching data from Redis')

# this will give all the hosts and IPs for all sites
# for site in r.smembers('sites'):
#     for host, ip in r.hgetall(site + b':hosts').items():
#         print(f'{host} ----> {r.smembers(ip)}')

# todo code for particular site

mysite = b'newark'
for host, ip in r.hgetall(mysite + b':hosts').items():
        print(f'{host} ----> {r.smembers(ip)}')
