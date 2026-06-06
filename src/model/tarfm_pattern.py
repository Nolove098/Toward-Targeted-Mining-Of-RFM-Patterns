from typing import Set

class TaRFMPattern:
    """Pattern đầu ra thỏa mãn đủ 4 điều kiện: Qi, R, F, M."""
    def __init__(self, items: Set[str], recency: float, frequency: int, monetary: float):
        self.items = items
        self.recency = recency
        self.frequency = frequency
        self.monetary = monetary

    def get_items(self) -> Set[str]:
        return self.items

    def get_recency(self) -> float:
        return self.recency

    def get_frequency(self) -> int:
        return self.frequency

    def get_monetary(self) -> float:
        return self.monetary

    def size(self) -> int:
        return len(self.items)

    def __str__(self):
        # Format giống Java: Pattern[A, B, F]  R=1.84  F=2  M=476.00
        # items nên in dưới dạng list để dễ đọc giống Java
        items_list = list(self.items)
        # Sắp xếp items_list nếu muốn in đẹp
        return f"Pattern{items_list}  R={self.recency:.2f}  F={self.frequency}  M={self.monetary:.2f}"
    
    def __eq__(self, other):
        if not isinstance(other, TaRFMPattern):
            return False
        return self.items == other.items and self.frequency == other.frequency

    def __hash__(self):
        return hash((frozenset(self.items), self.frequency))
