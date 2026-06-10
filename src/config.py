import os

# sentence-transformers uses PyTorch; tell transformers to skip its TensorFlow
# backend so it doesn't fail on the Keras 3 / tf-keras incompatibility.
# Must be set before transformers is imported (config is imported first).
os.environ.setdefault("USE_TF", "0")

from dotenv import load_dotenv

load_dotenv()

# Project root is one level above this file (src/)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- LLM ---
LLM_MODEL = "llama-3.3-70b-versatile"

# --- Embeddings ---
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --- Vector store ---
CHROMA_COLLECTION = "rulesbot"
CHROMA_PATH = os.path.join(_PROJECT_ROOT, "chroma_db")

# --- Retrieval ---
N_RESULTS = 5

# --- Documents ---
DOCS_PATH = os.path.join(_PROJECT_ROOT, "documents")
REVIEWS_PATH = os.path.join(DOCS_PATH, "professor_reviews")

# --- Chunking ---
MAX_CHARS = 1000      # target chunk size (~256 tokens)
OVERLAP_CHARS = 200   # overlap carried between chunks (~50 tokens, ~20%)

