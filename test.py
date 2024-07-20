import os
import json
from dotenv import load_dotenv

# Load .env file
load_dotenv("./.env")

admin_credentials = json.loads(os.getenv("ADMIN_CREDENTIALS"))