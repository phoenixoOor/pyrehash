from abc import ABC, abstractmethod
from typing import Optional

class HashAlgorithm(ABC):
    """Base class for all hash algorithms."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the algorithm."""
        pass

    @property
    @abstractmethod
    def digest_size(self) -> int:
        """Return the digest size in bytes."""
        pass

    @abstractmethod
    def hash(self, data: str, salt: Optional[str] = None, salt_position: str = "prefix") -> str:
        """Compute the hash of the given data."""
        pass

    @abstractmethod
    def verify(self, data: str, hashed: str, salt: Optional[str] = None, salt_position: str = "prefix") -> bool:
        """Verify the data against the hash."""
        pass
