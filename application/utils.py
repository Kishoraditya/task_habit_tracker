import uuid
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def generate_referral_link(user_id: int) -> str:
    """
    Generates a simple, shareable referral link for a given user.
    In a real system, you'd have a user-specific code in DB.
    """
    unique_code = str(uuid.uuid4())[:8]
    # For demonstration, we embed user_id in the link.
    return f"https://yourapp.example.com/referral?user_id={user_id}&code={unique_code}"

import json
import requests

IPFS_API_URL = "http://127.0.0.1:5001/api/v0"


def store_task_on_ipfs(task_data):
    """Store a task on IPFS and return the hash."""
    file_content = json.dumps(task_data).encode()
    files = {"file": file_content}

    try:
        response = requests.post(f"{IPFS_API_URL}/add", files=files)
        response.raise_for_status()
        return response.json().get("Hash", "")
    except requests.exceptions.RequestException as e:
        print(f"IPFS Error: {e}")
        return ""


def retrieve_task_from_ipfs(ipfs_hash):
    """Retrieve task data from IPFS using the given hash."""
    try:
        response = requests.get(f"{IPFS_API_URL}/cat?arg={ipfs_hash}")
        response.raise_for_status()
        return json.loads(response.text)
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        print(f"IPFS Retrieval Error: {e}")
        return None
