from typing import List, Dict, Set

class Transaction:
    def __init__(self, tid: int):
        self.tid = tid
        self.items: List[str] = []
        self.item_utilities: Dict[str, float] = {}
        self.transaction_utility: float = 0.0

    def add_item(self, item: str, utility: float):
        self.items.append(item)
        self.item_utilities[item] = utility
        self.transaction_utility += utility

    def get_items(self) -> List[str]:
        return self.items

    def get_tid(self) -> int:
        return self.tid

    def get_transaction_utility(self) -> float:
        return self.transaction_utility

    def get_item_utility(self, item: str) -> float:
        return self.item_utilities.get(item, 0.0)

    def contains_all(self, query_items: Set[str]) -> bool:
        return query_items.issubset(set(self.items))

    def __str__(self):
        return f"Transaction(tid={self.tid}, items={self.items}, TU={self.transaction_utility})"
