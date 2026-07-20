import requests
import base64
import io
from PIL import Image
from config import Config
from error_handler import retry_with_backoff, handle_api_error

class ImageGenerator:
    def __init__(self):
        self.config = Config()
        self.session = requests.Session()
    
    @retry_with_backoff
    def generate_image(self, prompt, width=1024, height=1024, samples=1):
        if not prompt or len(prompt.strip()) == 0:
            raise ValueError("Prompt cannot be empty!")
        
        print(f"🎨 Generating image for: '{prompt[:50]}...'")
        print(f"📐 Resolution: {width}x{height}")
        
        if self.config.API_PROVIDER == 'stability':
            return self._generate_stability(prompt, width, height, samples)
        elif self.config.API_PROVIDER == 'openai':
            return self._generate_openai(prompt, width, height, samples)
        else:
            raise ValueError(f"Unsupported API provider: {self.config.API_PROVIDER}")
    
    def _generate_stability(self, prompt, width, height, samples):
        headers = {
            "Authorization": f"Bearer {self.config.STABILITY_API_KEY}",
            "Content-Type": "application/json"
        }
        
        if not self.config.STABILITY_API_KEY:
            raise ValueError("STABILITY_API_KEY not found! Please add it to .env file")
        
        payload = {
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "height": height,
            "width": width,
            "samples": samples,
            "style_preset": "photographic"
        }
        
        print("📤 Sending request to Stability AI...")
        
        response = self.session.post(
            self.config.STABILITY_URL,
            json=payload,
            headers=headers,
            timeout=(self.config.CONNECTION_TIMEOUT, self.config.READ_TIMEOUT)
        )
        
        handle_api_error(response)
        
        if response.status_code == 200:
            data = response.json()
            if "artifacts" in data and len(data["artifacts"]) > 0:
                image_data = data["artifacts"][0]["base64"]
                image_bytes = base64.b64decode(image_data)
                image = Image.open(io.BytesIO(image_bytes))
                print("✅ Image generated successfully!")
                return image
            else:
                raise Exception("No image data received from API")
        else:
            raise Exception(f"API returned status {response.status_code}: {response.text}")
    
    def _generate_openai(self, prompt, width, height, samples):
        headers = {
            "Authorization": f"Bearer {self.config.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        if not self.config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found! Please add it to .env file")
        
        size_map = {
            (1024, 1024): "1024x1024",
            (1792, 1024): "1792x1024",
            (1024, 1792): "1024x1792"
        }
        size = size_map.get((width, height), "1024x1024")
        
        payload = {
            "model": "dall-e-3",
            "prompt": prompt,
            "n": min(samples, 1),
            "size": size,
            "quality": "standard"
        }
        
        print("📤 Sending request to OpenAI...")
        
        response = self.session.post(
            self.config.OPENAI_URL,
            json=payload,
            headers=headers,
            timeout=(self.config.CONNECTION_TIMEOUT, self.config.READ_TIMEOUT)
        )
        
        handle_api_error(response)
        
        if response.status_code == 200:
            data = response.json()
            image_url = data["data"][0]["url"]
            img_response = requests.get(image_url, timeout=30)
            image = Image.open(io.BytesIO(img_response.content))
            print("✅ Image generated successfully!")
            return image
        else:
            raise Exception(f"API returned status {response.status_code}: {response.text}")