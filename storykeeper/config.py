from pathlib import Path

# Directorio raíz del proyecto.
BASE_DIR = Path(__file__).resolve().parent.parent

# Modelos locales disponibles en Ollama.
GENERATION_MODEL = "gemma3:4b"
EMBEDDING_MODEL = "nomic-embed-text"

# Configuración de ChromaDB.
CHROMA_DIR = BASE_DIR / ".chroma"
COLLECTION_NAME = "storykeeper_continuity"

# Recuperación.
TOP_K = 4
