from typing import Optional, Dict, Type
from ..algorithms.hash_algorithm import HashAlgorithm
from ..algorithms.md5 import MD5Algorithm
from ..algorithms.sha256 import SHA256Algorithm
from ..algorithms.bcrypt import BcryptAlgorithm

ALGORITHMS: Dict[str, Type[HashAlgorithm]] = {
    "md5": MD5Algorithm,
    "sha256": SHA256Algorithm,
    "bcrypt": BcryptAlgorithm,
}

HASH_LENGTHS: Dict[int, str] = {
    32: "md5",
    64: "sha256",
    60: "bcrypt",
}

def detect_algorithm(hash_str: str) -> Optional[str]:
    """Detect hash algorithm based on hex digest length."""
    length = len(hash_str)
    return HASH_LENGTHS.get(length)

def get_algorithm_instance(name: str) -> HashAlgorithm:
    """Get an instance of the specified hash algorithm."""
    if name not in ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {name}")
    return ALGORITHMS[name]()

class SaltManager:
    """Handles salt operations."""
    @staticmethod
    def apply(data: str, salt: Optional[str], position: str) -> str:
        if not salt:
            return data
        return f"{salt}{data}" if position == "prefix" else f"{data}{salt}"
