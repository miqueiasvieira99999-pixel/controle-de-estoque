from dotenv import dotenv_values
from pathlib import Path

ENV_FILE = Path(__file__).resolve().parent / ".env"

config = dotenv_values(ENV_FILE)

SUPABASE_URL = config.get("SUPABASE_URL")
SUPABASE_KEY = config.get("SUPABASE_KEY")