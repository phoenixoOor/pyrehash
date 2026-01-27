import time
from typing import Optional, List
from ..core.attack_engine import AttackEngine
from ..core.progress_manager import ProgressManager
from .dictionary_attack import DictionaryAttack

class HybridAttack(DictionaryAttack):
    """Dictionary attack with rules (e.g., adding numbers, leet speak)."""
    
    def apply_rules(self, password: str) -> List[str]:
        candidates = [password]
        # Rule 1: Suffixes
        for i in range(10):
            candidates.append(f"{password}{i}")
        # Rule 2: Leet speak (simple)
        leet_map = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'}
        leet_pass = "".join(leet_map.get(c.lower(), c) for c in password)
        if leet_pass != password:
            candidates.append(leet_pass)
        return candidates

    def run(self, file_path: str, salt: Optional[str] = None, salt_position: str = "prefix") -> Optional[str]:
        self.start_time = time.perf_counter()
        self.is_running = True
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            total_lines = sum(1 for _ in f)

        # Total is larger due to rules, but we'll stick to lines for simplicity or scale it
        progress = ProgressManager(total=total_lines, desc="Hybrid Attack")
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if not self.is_running:
                    break
                
                base_password = line.strip()
                candidates = self.apply_rules(base_password)
                
                for password in candidates:
                    self.attempts += 1
                    if self.algorithm.verify(password, self.target_hash, salt, salt_position):
                        self.result = password
                        self.is_running = False
                        break
                
                progress.update(1)
        
        progress.close()
        self.end_time = time.perf_counter()
        return self.result
