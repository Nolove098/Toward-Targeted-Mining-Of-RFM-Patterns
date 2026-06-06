from typing import List, Set
from src.model import Transaction, TaRFMPattern
from src.order import TWUCalculator, TaRFMOrder
from .get_rfm_list import GetRFMList
from .get_tarfm_patterns import GetTaRFMPatterns

class TaRFM:
    """
    Algorithm 1: TaRFM — Entry point.
    Điều phối toàn bộ quá trình khai thác.
    """

    def run(self, database: List[Transaction], query_items: Set[str],
            delta: float, gamma: float, alpha: float, beta: float) -> List[TaRFMPattern]:
        
        # Bước 1: Tính TWU (quét DB lần 1)
        twu_calc = TWUCalculator()
        twu_map = twu_calc.calculate(database)

        # Bước 2: Xây dựng TaRFM Order
        tarfm_order = TaRFMOrder(twu_map, query_items)
        print("TaRFM Order: " + str(tarfm_order))

        # Bước 3: Xây dựng RFM-List (quét DB lần 2, áp dụng Strategy 1)
        list_builder = GetRFMList(query_items, tarfm_order)
        rfm_list_map = list_builder.build(database)

        # Bước 4: Khai thác TaRFM Patterns (Strategies 2 & 3)
        if not database:
            return []
            
        tlast = max(tx.get_tid() for tx in database)
        db_size = len(database)

        miner = GetTaRFMPatterns(
            query_items, tarfm_order, gamma, alpha, beta, delta, db_size, tlast
        )

        rfm_list = list(rfm_list_map.values())
        miner.mine([], None, rfm_list)

        return miner.get_results()
