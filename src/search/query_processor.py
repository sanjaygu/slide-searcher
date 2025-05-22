from typing import List, Dict, Any
from src.embedding.text_embedder import TextEmbedder
from src.storage.weaviate_client import WeaviateClient

class QueryProcessor:
    def __init__(self):
        self.text_embedder = TextEmbedder()
        self.weaviate_client = WeaviateClient()

    def process_query(self, query: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Process a search query with optional filters.
        """
        # Generate query embedding
        query_embedding = self.text_embedder.generate_embedding(query)

        # Search in Weaviate
        results = self.weaviate_client.search_slides(query)

        # Apply filters if provided
        if filters:
            results = self._apply_filters(results, filters)

        return results

    def _apply_filters(self, results: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Apply filters to search results.
        """
        filtered_results = results
        for key, value in filters.items():
            filtered_results = [
                r for r in filtered_results
                if r.get(key) == value
            ]
        return filtered_results 