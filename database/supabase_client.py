
import os

from dotenv import load_dotenv
from supabase import create_client

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.abspath(
    os.path.join(CURRENT_DIR, "..")
)

ENV_PATH = os.path.join(PROJECT_ROOT, ".env")

load_dotenv(ENV_PATH)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL:
    raise Exception("SUPABASE_URL not found.")

if not SUPABASE_KEY:
    raise Exception("SUPABASE_SERVICE_ROLE_KEY not found.")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)
