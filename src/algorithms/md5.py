import hashlib
from typing import Optional
from .hash_algorithm import HashAlgorithm

class MD5Algorithm(HashAlgorithm):
    @property
    def name(self) -> str:
        return "md5"

    @property
    def digest_size(self) -> int:
        return 16

    def _apply_salt(self, data: str, salt: Optional[str], salt_position: str) -> str:
        if not salt:
            return data
        return f"{salt}{data}" if salt_position == "prefix" else f"{data}{salt}"

    def hash(self, data: str, salt: Optional[str] = None, salt_position: str = "prefix") -> str:
        salted_data = self._apply_salt(data, salt, salt_position)
        return hashlib.md5(salted_data.encode()).hexdigest()

    def verify(self, data: str, hashed: str, salt: Optional[str] = None, salt_position: str = "prefix") -> bool:
        return self.hash(data, salt, salt_position) == hashed.lower()
