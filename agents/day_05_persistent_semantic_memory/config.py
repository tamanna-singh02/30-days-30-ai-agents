
import sys
from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).parent
ROOT_DIR = BASE_DIR.parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from shared import MODEL_NAME

load_dotenv()

CHAT_MODEL = os.getenv("CHAT_MODEL", MODEL_NAME)
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

BASE_DIR = Path(__file__).parent

DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = DATA_DIR / "chroma"
SQLITE_DB = DATA_DIR / "memory.db"

DATA_DIR.mkdir(exist_ok=True)
CHROMA_DIR.mkdir(exist_ok=True)

