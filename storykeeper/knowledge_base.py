from pathlib import Path

import chromadb
import ollama

from storykeeper.config import (
    CHROMA_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    TOP_K,
)


class KnowledgeBase:
    """Gestiona la documentación y la recuperación semántica con ChromaDB."""

    def __init__(self):
        self.client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )

    @staticmethod
    def create_embedding(text: str) -> list[float]:
        response = ollama.embeddings(
            model=EMBEDDING_MODEL,
            prompt=text,
        )
        return response["embedding"]

    @staticmethod
    def split_into_chunks(document: str) -> list[str]:
        # En esta primera versión cada párrafo no vacío es un fragmento.
        return [
            paragraph.strip()
            for paragraph in document.split("\n\n")
            if paragraph.strip()
        ]

    def index_document(self, file_path: Path) -> int:
        if not file_path.exists():
            raise FileNotFoundError(f"No se encuentra el documento: {file_path}")

        document = file_path.read_text(encoding="utf-8")
        chunks = self.split_into_chunks(document)

        if not chunks:
            raise ValueError("El documento no contiene fragmentos para indexar.")

        # Reindexación completa para evitar duplicados al repetir el comando.
        existing = self.collection.get()
        if existing["ids"]:
            self.collection.delete(ids=existing["ids"])

        ids = [f"chunk_{index}" for index in range(len(chunks))]
        embeddings = [self.create_embedding(chunk) for chunk in chunks]
        metadatas = [
            {"source": file_path.name, "chunk": index}
            for index in range(len(chunks))
        ]

        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )
        return len(chunks)

    def retrieve(self, query: str, top_k: int = TOP_K) -> list[dict]:
        if self.collection.count() == 0:
            raise RuntimeError(
                "La base de conocimiento está vacía. Ejecuta primero: python main.py index"
            )

        query_embedding = self.create_embedding(query)
        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, self.collection.count()),
            include=["documents", "metadatas", "distances"],
        )

        retrieved = []
        for document, metadata, distance in zip(
            result["documents"][0],
            result["metadatas"][0],
            result["distances"][0],
        ):
            retrieved.append({
                "text": document,
                "source": metadata.get("source", "desconocido"),
                "chunk": metadata.get("chunk", -1),
                "distance": distance,
            })

        return retrieved
