# autoscaler/utils/retry.py
import time
from autoscaler.utils.logger import get_logger

logger = get_logger("retry")

def retry_on_failure(func, retries=3, delay=1):
    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            logger.error(f"Attempt {attempt+1} failed: {e}")
            time.sleep(delay)
            delay *= 2
    raise Exception("Operation failed after multiple retries")
