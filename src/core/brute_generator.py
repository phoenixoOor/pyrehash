import itertools
from typing import Iterable

def brute_force_generator(charset: str, min_length: int, max_length: int) -> Iterable[str]:
    """Generates password candidates for brute-force attack."""
    for length in range(min_length, max_length + 1):
        for combo in itertools.product(charset, repeat=length):
            yield "".join(combo)
