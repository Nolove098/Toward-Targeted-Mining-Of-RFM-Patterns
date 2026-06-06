from typing import Dict
import os

class UtilityReader:
    """Đọc external utility từ file"""
    
    def read(self, filepath: str) -> Dict[str, float]:
        utility_map = {}
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Utility file not found: {filepath}")
            
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split(':')
                if len(parts) == 2:
                    item_id = parts[0].strip()
                    price = float(parts[1].strip())
                    utility_map[item_id] = price
        return utility_map
