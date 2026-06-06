from typing import List, Dict, Set
from src.model import Transaction, RFMListNode, RFMTriple
from src.order import TaRFMOrder

class GetRFMList:
    """
    Algorithm 2: GetRFMList
    Quét database, áp dụng Strategy 1, xây dựng RFM-List theo TaRFM order.
    """

    def __init__(self, query_items: Set[str], order: TaRFMOrder):
        self.query_items = query_items
        self.order = order

    def build(self, database: List[Transaction]) -> Dict[str, RFMListNode]:
        """
        Xây dựng RFM-List từ database.
        @return Map: item → RFMListNode (chỉ 1-itemsets ở bước đầu)
        """
        # Dictionary trong Python >= 3.7 mặc định duy trì thứ tự chèn (giống LinkedHashMap)
        rfm_list: Dict[str, RFMListNode] = {}

        # Khởi tạo nodes theo TaRFM order
        for item in self.order.get_ordered_items():
            rfm_list[item] = RFMListNode([item])

        t = 0  # timestamp (= Tid)

        for tx in database:
            t += 1

            # Strategy 1: lọc giao dịch không chứa đủ Qi
            if not tx.contains_all(self.query_items):
                continue

            # Sắp xếp items theo TaRFM order
            sorted_items = self.order.sort_items(tx.get_items())

            # Tính tổng utility của giao dịch
            remaining_util = tx.get_transaction_utility()

            # Xây dựng triples cho từng item
            for item in sorted_items:
                iutil = tx.get_item_utility(item)
                remaining_util -= iutil  # remaining = utility của các items SAU item này

                node = rfm_list.get(item)
                if node is not None:
                    node.add_triple(RFMTriple(t, iutil, remaining_util))

        # Loại bỏ nodes rỗng
        keys_to_remove = [k for k, v in rfm_list.items() if len(v.get_triples()) == 0]
        for k in keys_to_remove:
            del rfm_list[k]

        return rfm_list
