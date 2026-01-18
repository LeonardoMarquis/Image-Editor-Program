import os
import cv2
from abc import ABC, abstractmethod
import numpy as np
from PIL import Image, ImageFilter, ImageOps


class Filter(ABC):
    
    # Classe para permitir Preview.
    
    @abstractmethod
    def simple_process(self, img_path):
        # só para retornar o objeto pillow image
        pass

    def apply(self, img_path):
        # aplica o filtro e salva a imagem no disco

        processed_img = self.simple_process(img_path)
        
        sufix = self.__class__.__name__.replace("Filter", "").lower()
        exit_name = self._generate_exit_name(img_path, sufix)
        
        processed_img.save(exit_name)
        return exit_name

    def _generate_exit_name(self, original_path, sufix):
        name, ext = os.path.splitext(original_path)
        return f"{name}_{sufix}{ext}"


# -- Basic Filters Pillow --

class GrayFilter(Filter):
    def simple_process(self, img_path):
        img = Image.open(img_path)
        return ImageOps.grayscale(img)

class BlackWhiteFilter(Filter):
    def simple_process(self, img_path):
        img = Image.open(img_path)
        img_cinza = ImageOps.grayscale(img)
        return img_cinza.point(lambda x: 0 if x < 128 else 255, '1')

class NegativeFilter(Filter):
    def simple_process(self, img_path):
        img = Image.open(img_path).convert("RGB")
        return ImageOps.invert(img)


class BlurredFilter(Filter):
    def simple_process(self, img_path):
        img = Image.open(img_path)
        return img.filter(ImageFilter.GaussianBlur(radius=5))

# -- Complex Filters OpenCV --

class ContourFilter(Filter):
    def simple_process(self, img_path):
        pil_img = Image.open(img_path).convert('RGB')
        cv_img = np.array(pil_img)
        cv_img = cv_img[:, :, ::-1].copy() 

        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        edges = cv2.Canny(blurred, 50, 150)
        edges_inverted = cv2.bitwise_not(edges)

        return Image.fromarray(edges_inverted)

class CartoonFilter(Filter):
    def simple_process(self, img_path):
        pil_img = Image.open(img_path).convert('RGB')
        cv_img = np.array(pil_img)
        cv_img = cv_img[:, :, ::-1].copy()

        color = cv2.bilateralFilter(cv_img, 9, 300, 300)
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 7)

        edges = cv2.adaptiveThreshold(gray, 
                                      255, 
                                      cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 
                                      9, 9)
        
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        cartoon_rgb = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
        
        return Image.fromarray(cartoon_rgb)