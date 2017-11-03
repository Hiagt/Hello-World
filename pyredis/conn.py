import redis

r = redis.Redis(host='localhost', port=6379, db=0)
r.set('test', 'test_redis_set')

print(r['test'])
