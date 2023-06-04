import os

from dotenv import load_dotenv
from redis.asyncio.client import Redis

load_dotenv()

redis = Redis(
    host=os.getenv('REDIS_HOST') or '127.0.0.1',
    password=os.getenv('REDIS_PASSWORD') or None,
    username=os.getenv('REDIS_USER') or None,
)
