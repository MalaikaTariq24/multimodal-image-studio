import time
import random
from functools import wraps
from config import Config

class RetryError(Exception):
    """Custom exception for retry failures"""
    pass

def retry_with_backoff(func):
    """
    Exponential Backoff with Jitter Decorator
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        config = Config()
        max_retries = config.MAX_RETRIES
        base_delay = config.BASE_DELAY
        max_delay = config.MAX_DELAY
        
        for attempt in range(max_retries):
            try:
                print(f"🔄 Attempt {attempt + 1}/{max_retries}...")
                return func(*args, **kwargs)
                
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"❌ All {max_retries} attempts failed!")
                    raise RetryError(f"Failed after {max_retries} retries: {str(e)}")
                
                delay = min(base_delay * (2 ** attempt), max_delay)
                jitter = random.uniform(0, 0.1 * delay)
                wait_time = delay + jitter
                
                print(f"⚠️ Attempt {attempt + 1} failed: {str(e)[:50]}...")
                print(f"⏳ Waiting {wait_time:.2f}s before retry...")
                time.sleep(wait_time)
        
        return None
    
    return wrapper

def handle_api_error(response):
    """Handle API response errors"""
    status_code = response.status_code
    
    if status_code == 200:
        return response
    elif status_code == 429:
        raise Exception("Too many requests. Please wait and try again.")
    elif status_code == 503:
        raise Exception("Service temporarily unavailable. Retrying...")
    elif status_code == 401 or status_code == 403:
        raise Exception("Invalid API key. Please check your credentials.")
    elif status_code >= 500:
        raise Exception(f"Server error: {status_code}")
    else:
        raise Exception(f"API Error {status_code}: {response.text}")