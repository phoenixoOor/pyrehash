from abc import ABC, abstractmethod
from typing import Optional, Any, Dict
import time
from .hash_utils import get_algorithm_instance
from ..algorithms.hash_algorithm import HashAlgorithm

class AttackEngine(ABC):
    """Abstract base class for all attack engines."""
    
    def __init__(self, target_hash: str, algorithm_name: str):
        self.target_hash = target_hash.lower()
        self.algorithm: HashAlgorithm = get_algorithm_instance(algorithm_name)
        self.is_running = False
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.attempts = 0
        self.result: Optional[str] = None

    @abstractmethod
    def run(self, **kwargs: Any) -> Optional[str]:
        """Execute the attack."""
        pass

    def stop(self):
        """Stop the attack."""
        self.is_running = False

    @property
    def elapsed_time(self) -> float:
        """Return elapsed time in seconds."""
        if self.start_time is None:
            return 0.0
        if self.end_time is None:
            return time.perf_counter() - self.start_time
        return self.end_time - self.start_time

    @property
    def speed(self) -> float:
        """Return speed in hashes per second."""
        elapsed = self.elapsed_time
        if elapsed == 0:
            return 0.0
        return self.attempts / elapsed
