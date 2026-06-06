from typing import List
from .rfm_triple import RFMTriple

class RFMListNode:
    """
    Một node trong RFM-List, tương ứng với một itemset X.
    Mỗi node lưu danh sách các triples (Tid, iutil, rutil).
    Xem Fig. 1 trong bài báo.
    """
    def __init__(self, itemset: List[str]):
        self.itemset = list(itemset)
        self.triples: List[RFMTriple] = []
        
        # Cache cho tổng utility (dùng trong Strategy 2)
        self.sum_iutil: float = 0.0
        self.sum_rutil: float = 0.0

    def add_triple(self, triple: RFMTriple):
        self.triples.append(triple)
        self.sum_iutil += triple.get_iutil()
        self.sum_rutil += triple.get_rutil()

    def get_total_utility_bound(self) -> float:
        """Tổng (iutil + rutil) — dùng cho Strategy 2 (Property 1)"""
        return self.sum_iutil + self.sum_rutil

    def get_frequency(self) -> int:
        """Tần suất = số lần xuất hiện = số triples"""
        return len(self.triples)

    def get_monetary(self) -> float:
        """Monetary = tổng iutil"""
        return self.sum_iutil

    def get_itemset(self) -> List[str]:
        return self.itemset

    def get_triples(self) -> List[RFMTriple]:
        return self.triples

    def __str__(self):
        return f"Node{{itemset={self.itemset}, freq={self.get_frequency()}, M={self.sum_iutil:.2f}}}"
