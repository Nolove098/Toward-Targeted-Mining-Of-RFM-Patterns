from typing import List, Dict
import os
from src.model import Transaction
from .utility_reader import UtilityReader

class DatabaseReader:
    """Đọc transactions từ file và kết hợp với external utility"""
    
    def read(self, tx_file: str, util_file: str) -> List[Transaction]:
        utility_reader = UtilityReader()
        utility_map = utility_reader.read(util_file)
        
        database = []
        if not os.path.exists(tx_file):
            raise FileNotFoundError(f"Transaction file not found: {tx_file}")
            
        with open(tx_file, 'r', encoding='utf-8') as f:
            tid = 1
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                    
                tx = Transaction(tid)
                items = line.split()
                
                for item_str in items:
                    parts = item_str.split(':')
                    if len(parts) == 2:
                        item_id = parts[0].strip()
                        qty = float(parts[1].strip())
                        
                        # Lấy external utility p(x)
                        price = utility_map.get(item_id, 0.0)
                        
                        # u(x, Tj) = p(x) * q(x)
                        item_utility = price * qty
                        
                        tx.add_item(item_id, item_utility)
                        
                database.append(tx)
                tid += 1
                
        return database
