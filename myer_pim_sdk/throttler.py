# throttler.py

import asyncio
import time
from typing import Optional

from leakybucket import LeakyBucket, AsyncLeakyBucket
from leakybucket.persistence import InMemoryLeakyBucketStorage

# Myer's API allows max 20 calls per minute = 20/60 = 0.333 calls per second
# We'll be conservative and use 18 calls per minute to account for timing variations
MYER_RATE_LIMIT_PER_MINUTE = 18
MYER_RATE_LIMIT_PER_SECOND = MYER_RATE_LIMIT_PER_MINUTE / 60.0  # ~0.3 calls per second

storage = InMemoryLeakyBucketStorage(
    max_rate=MYER_RATE_LIMIT_PER_SECOND,
    time_period=1.0
)


throttler = LeakyBucket(storage)
async_throttler = AsyncLeakyBucket(storage)