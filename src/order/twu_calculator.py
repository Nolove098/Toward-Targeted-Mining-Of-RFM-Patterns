from typing import List, Dict
from src.model import Transaction

class TWUCalculator:
    """
    Tính Transaction-Weighted Utility (TWU) cho mỗi item.
    Định nghĩa 2 trong bài báo.
    Chỉ cần quét database 1 lần.
    """
    
    def calculate(self, database: List[Transaction]) -> Dict[str, float]:
        """
        Trả về map: item → TWU(item)
        TWU(X) = Σ TU(Tj) với mọi Tj chứa X
        """
        twu_map: Dict[str, float] = {}
        
        for tx in database:
            tu = tx.get_transaction_utility()
            for item in tx.get_items():
                twu_map[item] = twu_map.get(item, 0.0) + tu
                
        return twu_map
