from typing import List, Dict, Set, Iterable

class TaRFMOrder:
    """
    Xây dựng TaRFM Order theo Định nghĩa 8 & 9 trong bài báo.
    
    Quy tắc ưu tiên:
      1. Special items (∈ Qi) > Regular items
      2. Trong cùng nhóm: TWU nhỏ hơn → priority cao hơn
      3. Order = giảm dần theo priority
    """
    
    def __init__(self, twu_map: Dict[str, float], query_items: Set[str]):
        self.ordered_items = self._build_order(twu_map, query_items)
        self.rank_map = {item: i for i, item in enumerate(self.ordered_items)}

    def _build_order(self, twu_map: Dict[str, float], qi: Set[str]) -> List[str]:
        specials = []
        regulars = []
        
        for item in twu_map.keys():
            if item in qi:
                specials.append(item)
            else:
                regulars.append(item)
                
        # TWU tăng dần → priority giảm dần (TWU nhỏ = priority cao)
        # Trong Python, sort() là stable, ta có thể sort theo twu_map[item]
        specials.sort(key=lambda x: twu_map[x])
        regulars.sort(key=lambda x: twu_map[x])
        
        return specials + regulars

    def rank_of(self, item: str) -> int:
        """Trả về rank (0 = ưu tiên cao nhất). Item không có trong order → float('inf')"""
        return self.rank_map.get(item, float('inf'))

    def is_higher_priority(self, a: str, b: str) -> bool:
        return self.rank_of(a) < self.rank_of(b)

    def sort_items(self, items: Iterable[str]) -> List[str]:
        """Sắp xếp items trong một giao dịch theo TaRFM order"""
        return sorted(items, key=self.rank_of)

    def get_ordered_items(self) -> List[str]:
        return self.ordered_items

    def __str__(self):
        return " > ".join(self.ordered_items)
