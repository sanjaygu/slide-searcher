import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from typing import List, Dict, Any
import json
import os
import numpy as np

class ImageEmbedder:
    def __init__(self, config_path: str = "config/embedding_config.json"):
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        self.model_name = config['image_embedding']['model']
        self.batch_size = config['image_embedding']['batch_size']
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize CLIP model and processor
        self.model = CLIPModel.from_pretrained(self.model_name).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(self.model_name)
        
        # Set model to evaluation mode
        self.model.eval()

    def generate_embeddings(self, image_paths: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of images.
        """
        # Load and preprocess images
        images = [Image.open(path) for path in image_paths]
        inputs = self.processor(images=images, return_tensors="pt", padding=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Generate embeddings
        with torch.no_grad():
            image_features = self.model.get_image_features(**inputs)
            image_features = image_features / image_features.norm(dim=1, keepdim=True)
        
        return image_features.cpu().numpy().tolist()

    def generate_embedding(self, image_path: str) -> List[float]:
        """
        Generate embedding for a single image.
        """
        return self.generate_embeddings([image_path])[0]

    def compute_similarity(self, image_path1: str, image_path2: str) -> float:
        """
        Compute similarity between two images.
        """
        embeddings = self.generate_embeddings([image_path1, image_path2])
        return np.dot(embeddings[0], embeddings[1]) 