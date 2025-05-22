import weaviate
from typing import List, Dict, Any
import json
import os

class WeaviateClient:
    def __init__(self, url: str = None):
        self.url = url or os.getenv("WEAVIATE_URL", "http://localhost:8080")
        self.client = weaviate.Client(self.url)
        self._initialize_schema()

    def _initialize_schema(self):
        """
        Initialize Weaviate schema if it doesn't exist.
        """
        schema_path = "config/weaviate_schema.json"
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        
        try:
            self.client.schema.create(schema)
        except weaviate.exceptions.UnexpectedStatusCodeException:
            # Schema might already exist
            pass

    def store_slide(self, slide_data: Dict[str, Any], text_embedding: List[float], image_embedding: List[float] = None):
        """
        Store a slide in Weaviate with its embeddings.
        """
        data_object = {
            "slideNumber": slide_data["slide_number"],
            "content": slide_data["text_content"],
            "presentationId": slide_data["presentation_id"],
            "imageUrl": slide_data.get("image_url", ""),
            "topics": slide_data.get("topics", [])
        }

        self.client.data_object.create(
            data_object=data_object,
            class_name="Slide",
            vector=text_embedding
        )

    def search_slides(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search slides using vector similarity.
        """
        result = (
            self.client.query
            .get("Slide", ["slideNumber", "content", "imageUrl", "topics"])
            .with_near_text({"concepts": [query]})
            .with_limit(limit)
            .do()
        )

        return result["data"]["Get"]["Slide"] 