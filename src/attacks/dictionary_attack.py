import os
import time
from typing import Optional, Any
from ..core.attack_engine import AttackEngine
from ..core.progress_manager import ProgressManager

class DictionaryAttack(AttackEngine):
    """Dictionary attack implementation."""
    
    def run(self, file_path: str, salt: Optional[str] = None, salt_position: str = "prefix") -> Optional[str]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dictionary file not found: {file_path}")

        self.start_time = time.perf_counter()
        self.is_running = True
        
        # Count total lines for progress bar
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            total_lines = sum(1 for _ in f)

        progress = ProgressManager(total=total_lines, desc="Dictionary Attack")
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if not self.is_running:
                    break
                
                password = line.strip()
                self.attempts += 1
                progress.update(1)
                
                if self.algorithm.verify(password, self.target_hash, salt, salt_position):
                    self.result = password
                    self.is_running = False
                    break
        
        progress.close()
        self.end_time = time.perf_counter()
        return self.result
