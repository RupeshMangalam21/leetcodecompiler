import os
import sys
import redis
from rq import Worker, Queue, Connection

# Add src to path
sys.path.append('/app/src')

# Redis connection settings
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_url = f'redis://{redis_host}:6379/0'

def main():
    try:
        conn = redis.from_url(redis_url)
        # Test connection
        conn.ping()
        print(f"Connected to Redis at {redis_host}")
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")
        return

    with Connection(conn):
        print("Worker is starting...")
        q = Queue()  # Default queue
        worker = Worker([q])
        worker.work()

if __name__ == '__main__':
    main()
