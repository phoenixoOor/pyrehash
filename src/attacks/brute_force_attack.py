import time
from typing import Optional, Any
from ..core.attack_engine import AttackEngine
from ..core.brute_generator import brute_force_generator
from ..core.progress_manager import ProgressManager

class BruteForceAttack(AttackEngine):
    """Brute-force attack implementation."""
    
    def run(self, charset: str, min_length: int, max_length: int, salt: Optional[str] = None, salt_position: str = "prefix") -> Optional[str]:
        self.start_time = time.perf_counter()
        self.is_running = True
        
        # Calculate total combinations
        total_combos = sum(len(charset) ** length for length in range(min_length, max_length + 1))
        progress = ProgressManager(total=total_combos, desc="Brute-force Attack")
        
        for password in brute_force_generator(charset, min_length, max_length):
            if not self.is_running:
                break
                
            self.attempts += 1
            progress.update(1)
            
            if self.algorithm.verify(password, self.target_hash, salt, salt_position):
                self.result = password
                self.is_running = False
                break
                
        progress.close()
        self.end_time = time.perf_counter()
        return self.result
