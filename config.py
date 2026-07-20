import os
from dotenv import load_dotenv

# .env file ko load karein
load_dotenv()

class Config:
    # ===== API KEYS =====
    STABILITY_API_KEY = os.getenv('STABILITY_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    API_PROVIDER = os.getenv('API_PROVIDER', 'stability')
    
    # ===== API ENDPOINTS =====
    STABILITY_URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    OPENAI_URL = "https://api.openai.com/v1/images/generations"
    
    # ===== TIMEOUT SETTINGS (Project Requirement) =====
    CONNECTION_TIMEOUT = 3.05   # TCP connection timeout
    READ_TIMEOUT = 60           # Read timeout for slow generation
    
    # ===== RETRY SETTINGS =====
    MAX_RETRIES = 3
    BASE_DELAY = 1
    MAX_DELAY = 60
    
    # ===== IMAGE DEFAULTS =====
    DEFAULT_WIDTH = 1024
    DEFAULT_HEIGHT = 1024
    DEFAULT_SAMPLES = 1
    
    # ===== QUALITY THRESHOLDS =====
    AESTHETIC_THRESHOLD = 7.0
    SEMANTIC_THRESHOLD = 0.7