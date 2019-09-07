from rediscluster import RedisCluster

startup_nodes = [
    {
        'host': "10.0.0.13",
        'port': 6379
    },
        {
        'host': "10.0.0.12",
        'port': 7000
    }
]

client = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)


print(client.get("name"))