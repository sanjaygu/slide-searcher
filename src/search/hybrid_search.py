from typing import List, Dict, Any
from src.search.query_processor import QueryProcessor
from src.storage.weaviate_client import WeaviateClient

class HybridSearch:
    def __init__(self):
        self.query_processor = QueryProcessor()
        self.weaviate_client = WeaviateClient()

    def search(self, query: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Perform hybrid search combining vector and keyword search.
        """
        # Vector search
        vector_results = self.query_processor.process_query(query, filters)

        # Keyword search (using Weaviate's bm25)
        keyword_results = self.weaviate_client.search_slides(
            query,
            search_type="bm25"
        )

        # Combine and rank results
        combined_results = self._combine_results(vector_results, keyword_results)
        return combined_results

    def _combine_results(self, vector_results: List[Dict[str, Any]], 
                        keyword_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Combine and rank results from different search methods.
        """
        # Simple implementation - can be enhanced with better ranking
        seen_ids = set()
        combined = []

        for result in vector_results + keyword_results:
            result_id = result.get("id")
            if result_id not in seen_ids:
                seen_ids.add(result_id)
                combined.append(result)

        return combined 