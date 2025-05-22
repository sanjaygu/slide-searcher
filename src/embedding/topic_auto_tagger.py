from typing import List, Dict, Any
import json
import os
from openai import OpenAI
import numpy as np
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer

class TopicAutoTagger:
    def __init__(self, config_path: str = "config/embedding_config.json"):
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        self.model = config['topic_extraction']['model']
        self.max_topics = config['topic_extraction']['max_topics']
        self.confidence_threshold = config['topic_extraction']['confidence_threshold']
        self.client = OpenAI()
        
        # Initialize sentence transformer for clustering
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

    def extract_topics(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract topics from text using LLM and clustering.
        """
        # Split text into sentences
        sentences = self._split_into_sentences(text)
        
        if len(sentences) < self.max_topics:
            return self._extract_topics_llm(text)
        
        # Generate embeddings for sentences
        embeddings = self.embedder.encode(sentences)
        
        # Cluster sentences
        clusters = self._cluster_sentences(embeddings)
        
        # Extract topics from clusters
        topics = self._extract_topics_from_clusters(sentences, clusters)
        
        return topics

    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        import nltk
        nltk.download('punkt', quiet=True)
        return nltk.sent_tokenize(text)

    def _cluster_sentences(self, embeddings: np.ndarray) -> np.ndarray:
        """Cluster sentences using K-means."""
        kmeans = KMeans(n_clusters=self.max_topics, random_state=42)
        return kmeans.fit_predict(embeddings)

    def _extract_topics_from_clusters(self, sentences: List[str], clusters: np.ndarray) -> List[Dict[str, Any]]:
        """Extract topics from sentence clusters."""
        topics = []
        for cluster_id in range(self.max_topics):
            cluster_sentences = [s for s, c in zip(sentences, clusters) if c == cluster_id]
            if cluster_sentences:
                # Use LLM to generate topic from cluster
                topic = self._generate_topic_from_cluster(cluster_sentences)
                if topic:
                    topics.append({
                        'topic': topic,
                        'confidence': self._calculate_cluster_confidence(cluster_sentences)
                    })
        return topics

    def _generate_topic_from_cluster(self, sentences: List[str]) -> str:
        """Generate topic from cluster using LLM."""
        prompt = f"""
        Generate a concise topic that represents the following sentences:
        {chr(10).join(sentences)}
        Topic should be 1-3 words.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a topic extraction assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content.strip()

    def _calculate_cluster_confidence(self, sentences: List[str]) -> float:
        """Calculate confidence score for a cluster."""
        # Simple implementation based on cluster size and coherence
        return min(1.0, len(sentences) / 5)

    def _extract_topics_llm(self, text: str) -> List[Dict[str, Any]]:
        """Extract topics using LLM for short texts."""
        prompt = f"""
        Extract up to {self.max_topics} main topics from the following text.
        For each topic, provide a confidence score between 0 and 1.
        Text: {text}
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a topic extraction assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        # Parse response and filter by confidence threshold
        topics = self._parse_topics(response.choices[0].message.content)
        return [t for t in topics if t['confidence'] >= self.confidence_threshold]

    def _parse_topics(self, response: str) -> List[Dict[str, Any]]:
        """Parse topics from LLM response."""
        # This is a simple implementation. You might want to enhance it
        # based on your specific needs and response format.
        lines = response.strip().split('\n')
        topics = []
        
        for line in lines:
            if ':' in line:
                topic, confidence = line.split(':')
                try:
                    confidence = float(confidence.strip())
                    topics.append({
                        'topic': topic.strip(),
                        'confidence': confidence
                    })
                except ValueError:
                    continue
        
        return topics 