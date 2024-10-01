import time
from celery import Celery
from celery.utils.log import get_task_logger
import redis

logger = get_task_logger(__name__)

app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')
cache = redis.StrictRedis(host='redis', port=6379, db=0)

@app.task()
def count_prime_factors(n):
    cached_result = cache.get(n)
    str_n = str(n)
    print(f"CACHED RESULT : {cached_result}")
    if cached_result:
        print(cached_result)
        return cached_result.decode('utf-8')
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1

    for i in range(3, int(n**0.5) + 1, 2):
        while n % i == 0:
            n //= i
            count += 1

    if n > 2:
        count += 1
        
    time.sleep(20)
    cache.set(str_n, str(count), ex=600)
    return count