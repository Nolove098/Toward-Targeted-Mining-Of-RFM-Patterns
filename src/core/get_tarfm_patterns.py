from typing import List, Set, Dict
import math
from src.model import Transaction, RFMListNode, RFMTriple, TaRFMPattern
from src.order import TaRFMOrder

class GetTaRFMPatterns:
    """
    Algorithm 3: GetTaRFMPatterns
    Khai thác đệ quy theo depth-first, áp dụng Strategy 2 & 3.
    """

    def __init__(self, query_items: Set[str], order: TaRFMOrder,
                 gamma: float, alpha: float, beta: float,
                 delta: float, db_size: int, tlast: int):
        self.query_items = query_items
        self.order = order
        self.gamma = gamma
        self.alpha = alpha
        self.beta = beta
        self.delta = delta
        self.db_size = db_size
        self.tlast = tlast
        self.results: List[TaRFMPattern] = []

    def mine(self, prefix: List[str], p_node: RFMListNode, rfm_list: List[RFMListNode]):
        """
        Hàm đệ quy chính.
        @param prefix   Pattern prefix hiện tại
        @param p_node   P-Node tương ứng với prefix (None nếu prefix rỗng)
        @param rfm_list Danh sách các node cần xét
        """
        for i in range(len(rfm_list)):
            node_x = rfm_list[i]

            # Tạo prefix mới = prefix + X.item
            new_prefix = list(prefix)
            new_prefix.append(node_x.get_itemset()[-1])

            # Strategy 3: lọc pattern ngắn hơn |Qi|
            if len(new_prefix) >= len(self.query_items):

                # Kiểm tra điều kiện F, M, R
                freq = node_x.get_frequency()
                monetary = node_x.get_monetary()
                recency = self._calc_recency(node_x)

                if freq >= int(self.db_size * self.alpha) and monetary >= self.beta and recency >= self.gamma:
                    # Là TaRFM pattern
                    self.results.append(TaRFMPattern(
                        set(new_prefix), recency, freq, monetary
                    ))

            # Strategy 2: utility bound pruning
            if node_x.get_total_utility_bound() < self.beta:
                continue  # Không thể cải thiện → bỏ qua

            # Xây dựng RFM-List mới bằng cách giao node_x với các nodes sau
            new_rfm_list = []
            for j in range(i + 1, len(rfm_list)):
                node_y = rfm_list[j]
                node_xy = self._intersect(node_x, node_y, p_node)
                if node_xy is not None and len(node_xy.get_triples()) > 0:
                    new_rfm_list.append(node_xy)

            # Đệ quy mine các patterns dài hơn
            if new_rfm_list:
                self.mine(new_prefix, node_x, new_rfm_list)

            # Strategy 2 (Property 2): sau khi mine xong item cuối của Qi,
            # các items sau không thể hình thành pattern chứa đủ Qi
            current_item = node_x.get_itemset()[-1]
            if self._is_last_query_item(current_item, prefix):
                break

    def _intersect(self, node_x: RFMListNode, node_y: RFMListNode, p_node: RFMListNode) -> RFMListNode:
        """
        Giao hai RFM-List nodes: X ∩ Y → XY
        Tìm Tid chung, tính iutil và rutil mới.
        Sử dụng thuật toán hai con trỏ tối ưu hóa vì triples được sắp xếp theo tid tăng dần.
        """
        new_itemset = list(node_x.get_itemset())
        new_itemset.append(node_y.get_itemset()[-1])

        node_xy = RFMListNode(new_itemset)

        x_triples = node_x.get_triples()
        y_triples = node_y.get_triples()
        p_triples = p_node.get_triples() if p_node is not None else []

        i, j, k = 0, 0, 0
        len_x, len_y, len_p = len(x_triples), len(y_triples), len(p_triples)

        while i < len_x and j < len_y:
            tx = x_triples[i]
            ty = y_triples[j]
            tid_x = tx.get_tid()
            tid_y = ty.get_tid()

            if tid_x == tid_y:
                if p_node is None:
                    new_iutil = tx.get_iutil() + ty.get_iutil()
                else:
                    p_iutil = 0.0
                    while k < len_p:
                        tp = p_triples[k]
                        tid_p = tp.get_tid()
                        if tid_p == tid_x:
                            p_iutil = tp.get_iutil()
                            break
                        elif tid_p < tid_x:
                            k += 1
                        else:
                            break
                    new_iutil = tx.get_iutil() + ty.get_iutil() - p_iutil

                new_rutil = ty.get_rutil()
                node_xy.add_triple(RFMTriple(tid_x, new_iutil, new_rutil))
                i += 1
                j += 1
            elif tid_x < tid_y:
                i += 1
            else:
                j += 1

        return node_xy

    def _calc_recency(self, node: RFMListNode) -> float:
        """Tính recency score của một node: R(X) = Σ (1-δ)^(Tlast - Tid)"""
        r = 0.0
        for triple in node.get_triples():
            r += math.pow(1.0 - self.delta, self.tlast - triple.get_tid())
        return r

    def _is_last_query_item(self, item: str, prefix: List[str]) -> bool:
        """
        Kiểm tra xem item hiện tại có phải là query item cuối cùng
        chưa xuất hiện trong prefix không.
        Nếu đúng → sau khi mine xong, dừng (Strategy 2 / Property 2).
        """
        if item not in self.query_items:
            return False
        covered = set(prefix)
        covered.add(item)
        return self.query_items.issubset(covered)

    def get_results(self) -> List[TaRFMPattern]:
        return self.results
