from qdrant_client.models import Distance, VectorParams, PointStruct
from app.db.qdrant import qdrant
from app.core.constants import EMBEDDING_COLLECTION, AGENT_MEMORY_COLLECTION
import uuid

class QdrantService:
    def __init__(self):
        self.collection = EMBEDDING_COLLECTION
        self.agent_memory_collection = AGENT_MEMORY_COLLECTION
        self._ensure_collection(self.collection)
        self._ensure_collection(self.agent_memory_collection)

    def _ensure_collection(self, collection_name: str):
        collections = [c.name for c in qdrant.get_collections().collections]

        if collection_name not in collections:
            qdrant.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )

    def upsert_candidate_embedding(self, candidate_id: int, vector: list, payload: dict):
        qdrant.upsert(
            collection_name=self.collection,
            points=[
                PointStruct(
                    id=candidate_id,
                    vector=vector,
                    payload=payload
                )
            ]
        )

    def search_similar(self, vector: list, limit: int = 5):
        results = qdrant.query_points(
            collection_name=self.collection,
            query=vector,
            limit=limit
        )
        return results.points if results and results.points else []
        
    def store_evaluator_memory(self, vector: list, payload: dict):
        qdrant.upsert(
            collection_name=self.agent_memory_collection,
            points=[
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload=payload
                )
            ]
        )
    def search_evaluator_memory(self, vector: list, limit: int = 1):
        results = qdrant.query_points(
            collection_name=self.agent_memory_collection,
            query=vector,
            limit=limit
        )
        return results.points if results and results.points else []
    

qdrant_service = QdrantService()