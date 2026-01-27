import bcrypt
from typing import Optional
from .hash_algorithm import HashAlgorithm

class BcryptAlgorithm(HashAlgorithm):
    @property
    def name(self) -> str:
        return "bcrypt"

    @property
    def digest_size(self) -> int:
        return 23  # Typically 23 bytes binary, but we deal with strings

    def hash(self, data: str, salt: Optional[str] = None, salt_position: str = "prefix") -> str:
        # bcrypt handles its own salt in the hash string
        return bcrypt.hashpw(data.encode(), bcrypt.gensalt()).decode()

    def verify(self, data: str, hashed: str, salt: Optional[str] = None, salt_position: str = "prefix") -> bool:
        try:
            return bcrypt.checkpw(data.encode(), hashed.encode())
        except Exception:
            return False
