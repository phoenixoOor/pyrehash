import time
from typing import Optional, List
from ..core.attack_engine import AttackEngine
from ..core.progress_manager import ProgressManager
from .dictionary_attack import DictionaryAttack

class HybridAttack(DictionaryAttack):
    """Dictionary attack with rules (e.g., adding numbers, leet speak)."""
    
    def get_leet_combinations(self, word: str) -> set[str]:
        """Generate all possible leet combinations for a word."""
        leet_map = {
            'a': ['4', '@'],
            'e': ['3'],
            'i': ['1', '!'],
            'o': ['0'],
            's': ['5', '$'],
            't': ['7'],
            'b': ['8']
        }
        
        results = {word}
        
        def evolve(current_word: str, index: int):
            if index >= len(current_word):
                return
            
            char = current_word[index].lower()
            if char in leet_map:
                for replacement in leet_map[char]:
                    # Create new version with replacement at current index
                    new_word = current_word[:index] + replacement + current_word[index+1:]
                    results.add(new_word)
                    # Continue evolving from the next character
                    evolve(new_word, index + 1)
            
            # Also continue evolving without replacement at current index
            evolve(current_word, index + 1)

        evolve(word, 0)
        return results

    def apply_rules(self, password: str) -> List[str]:
        """Apply a combinatorial pipeline of rules to a password."""
        # 1. Base variations
        base_vars = {password, password.lower(), password.capitalize(), password.upper()}
        
        # 2. Generate ALL leet combinations for each base variation
        all_leet = set()
        for base in base_vars:
            all_leet.update(self.get_leet_combinations(base))
        
        # 3. Apply suffixes to ALL leet variations
        suffixes = ["", "!", "!!", "123", "123456", "12345678", "123456789"]
        
        # Add years (from 2010 to 2026)
        for year in range(2010, 2027):
            suffixes.append(str(year))
            
        for i in range(10):
            suffixes.append(str(i))
            
        final_candidates = set()
        for v in all_leet:
            for s in suffixes:
                final_candidates.add(f"{v}{s}")
        
        return list(final_candidates)

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
                        progress.complete()
                        break
                
                if not self.is_running:
                    break
                progress.update(1)
        
        progress.close()
        self.end_time = time.perf_counter()
        return self.result
