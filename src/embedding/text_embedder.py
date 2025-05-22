from sentence_transformers import SentenceTransformer
import torch
from typing import List, Dict, Any
import json
import os
import numpy as np
from transformers import AutoTokenizer, AutoModel

class TextEmbedder:
    def __init__(self, config_path: str = "config/embedding_config.json"):
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        self.model_name = config['text_embedding']['model']
        self.batch_size = config['text_embedding']['batch_size']
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name).to(self.device)
        
        # Set model to evaluation mode
        self.model.eval()

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        """
        # Tokenize texts
        encoded = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt"
        ).to(self.device)
        
        # Generate embeddings
        with torch.no_grad():
            outputs = self.model(**encoded)
            embeddings = self._mean_pooling(outputs, encoded['attention_mask'])
        
        return embeddings.cpu().numpy().tolist()

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        """
        return self.generate_embeddings([text])[0]

    def _mean_pooling(self, model_output, attention_mask):
        """
        Perform mean pooling on token embeddings.
        """
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 0) / torch.clamp(input_mask_expanded.sum(0), min=1e-9) 