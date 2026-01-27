import time
from ..core.hash_utils import get_algorithm_instance
from .color_output import log_info

def run_benchmark(algorithm_name: str, duration: int = 5):
    """Benchmark hash performance for a specific algorithm."""
    algorithm = get_algorithm_instance(algorithm_name)
    log_info(f"Benchmarking {algorithm_name} for {duration} seconds...")
    
    attempts = 0
    start = time.perf_counter()
    test_data = "password123"
    
    while time.perf_counter() - start < duration:
        algorithm.hash(test_data)
        attempts += 1
        
    elapsed = time.perf_counter() - start
    speed = attempts / elapsed
    log_info(f"Results for {algorithm_name}: {speed:.2f} hashes/sec")
    return speed
