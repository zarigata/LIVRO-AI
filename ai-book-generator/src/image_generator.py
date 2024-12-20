import torch
import json
from diffusers import StableDiffusionPipeline
from PIL import Image
import base64
import io
import os

class ImageGenerator:
    def __init__(self, config_path='../config.json'):
        """
        Initialize Stable Diffusion image generation pipeline
        
        Args:
            config_path (str): Path to configuration file
        """
        # Load configuration
        with open(config_path, 'r') as config_file:
            self.config = json.load(config_file)
        
        # Configure Stable Diffusion
        sd_config = self.config['stable_diffusion']
        model_id = sd_config.get('default_model', "stabilityai/stable-diffusion-xl-base-1.0")
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipeline = StableDiffusionPipeline.from_pretrained(
            model_id, 
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        ).to(self.device)
    
    def analyze_art_style(self, user_image_path: str) -> str:
        """
        Analyze the art style of the uploaded user image
        
        Args:
            user_image_path (str): Path to the uploaded image
        
        Returns:
            str: Descriptive art style prompt
        """
        # Placeholder for advanced art style transfer
        # In a real implementation, use computer vision techniques
        art_styles = self.config['art_styles']['custom_styles']
        return list(art_styles.values())[0]  # Return first custom style
    
    def generate_illustration(self, 
                               prompt: str, 
                               negative_prompt: str = "", 
                               num_inference_steps: int = 50) -> Image:
        """
        Generate an illustration based on text prompt
        
        Args:
            prompt (str): Detailed description for image generation
            negative_prompt (str): Description of what to avoid
            num_inference_steps (int): Quality and detail level
        
        Returns:
            Image: Generated illustration
        """
        image = self.pipeline(
            prompt=prompt,
            negative_prompt=negative_prompt or "low quality, blurry, bad composition",
            num_inference_steps=num_inference_steps
        ).images[0]
        
        return image
    
    def image_to_base64(self, image: Image) -> str:
        """
        Convert PIL Image to base64 string
        
        Args:
            image (Image): PIL Image object
        
        Returns:
            str: Base64 encoded image
        """
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Example usage
if __name__ == "__main__":
    generator = ImageGenerator()
    art_style = generator.analyze_art_style("user_photo.jpg")
    illustration = generator.generate_illustration(
        f"A magical scene in {art_style} style"
    )
    illustration.save("generated_illustration.png")
