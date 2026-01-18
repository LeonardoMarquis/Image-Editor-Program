import os
import requests
import shutil
from PIL import Image as PILImage

class Download:
    def download_img(self, url):
        print(f"Starting download from: {url}")
        
        try:
            # simple requirement
            resposta = requests.get(url, stream=True)
            resposta.raise_for_status()

            target_name = "target_image.jpg"

            with open(target_name, 'wb') as arquivo_saida:
                resposta.raw.decode_content = True
                shutil.copyfileobj(resposta.raw, arquivo_saida)
            
            return target_name

        except Exception as e:
            raise Exception(f"Download Error! : {e}")

class Image:
    def __init__(self, path):
        self.path = path
        self.validate_exists()

    def validate_exists(self):
        
        # to verify if file exists
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"File not found! : {self.path}")
        
        # Open with PIL to verify if it's an image
        try:
            with PILImage.open(self.path) as img:
                img.verify() 
        except Exception:
            raise ValueError("The file is not a valid image!")
        
        return True