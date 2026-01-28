from tqdm import tqdm
from typing import Optional

class ProgressManager:
    """Manages progress bars for attacks."""
    
    def __init__(self, total: Optional[int] = None, desc: str = "Cracking"):
        self.pbar = tqdm(total=total, desc=desc, unit="hash")

    def update(self, n: int = 1):
        self.pbar.update(n)

    def complete(self):
        """Force the progress bar to 100%."""
        self.pbar.n = self.pbar.total
        self.pbar.refresh()

    def close(self):
        self.pbar.close()

    def set_description(self, desc: str):
        self.pbar.set_description(desc)
