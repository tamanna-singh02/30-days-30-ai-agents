"""Configuration settings for Safe SQL Agent."""

from shared.config import DATABASE_URL as SHARED_DATABASE_URL
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")