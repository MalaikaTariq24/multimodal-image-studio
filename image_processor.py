from PIL import Image
import os
import time
from datetime import datetime

class ImageProcessor:
    def __init__(self, output_dir="outputs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "sample"), exist_ok=True)
    
    def validate_image(self, image):
        """CRITICAL: Force full pixel decode"""
        try:
            print("🔍 Validating image integrity...")
            image.load()
            print(f"✅ Image validated: {image.width}x{image.height}, {image.mode}")
            return True
        except OSError as e:
            print(f"❌ Image validation failed - Corrupted data stream: {e}")
            return False
        except Exception as e:
            print(f"❌ Image validation failed: {e}")
            return False
    
    def verify_image_file(self, filepath):
        """Verify saved image file integrity"""
        try:
            print(f"🔍 Verifying saved file: {filepath}")
            with Image.open(filepath) as img:
                img.load()
                file_size = os.path.getsize(filepath)
                if file_size < 1000:
                    print(f"⚠️ File too small: {file_size} bytes")
                    return False
                print(f"✅ File verified: {file_size} bytes")
                return True
        except OSError as e:
            print(f"❌ File verification failed - Corrupted: {e}")
            return False
        except Exception as e:
            print(f"❌ File verification failed: {e}")
            return False
    
    def save_image(self, image, filename=None):
        """Save image to disk with validation"""
        if filename is None:
            timestamp = int(time.time())
            filename = f"generated_{timestamp}.png"
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        save_dir = os.path.join(self.output_dir, date_str)
        os.makedirs(save_dir, exist_ok=True)
        
        filepath = os.path.join(save_dir, filename)
        print(f"💾 Saving image to: {filepath}")
        
        image.save(filepath, "PNG", optimize=True)
        
        if not self.verify_image_file(filepath):
            os.remove(filepath)
            raise Exception("File verification failed - corrupted image saved!")
        
        print(f"✅ Image saved successfully: {filepath}")
        return filepath
    
    def get_image_info(self, image):
        """Get image metadata"""
        return {
            "format": image.format or "PNG",
            "mode": image.mode,
            "size": image.size,
            "width": image.width,
            "height": image.height,
            "pixels": image.width * image.height,
            "color_channels": len(image.getbands())
        }
    
    def validate_resolution(self, width, height):
        """Validate resolution"""
        valid_resolutions = [
            (1024, 1024),
            (1344, 768),
            (768, 1344),
        ]
        
        if (width, height) in valid_resolutions:
            return True
        else:
            valid_sizes = [512, 768, 1024, 1344]
            if width in valid_sizes and height in valid_sizes:
                print(f"⚠️ Resolution {width}x{height} is not in standard list")
                return True
            else:
                print(f"❌ Invalid resolution: {width}x{height}")
                return False
    
    def create_thumbnail(self, image, size=(300, 300)):
        """Create thumbnail of image"""
        try:
            thumbnail = image.copy()
            thumbnail.thumbnail(size, Image.Resampling.LANCZOS)
            return thumbnail
        except Exception as e:
            print(f"❌ Thumbnail creation failed: {e}")
            return None