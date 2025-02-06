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
