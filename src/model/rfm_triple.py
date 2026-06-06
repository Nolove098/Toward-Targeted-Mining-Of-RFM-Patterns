class RFMTriple:
    """
    Tuple (Tid, iutil, rutil) trong RFM-List.
    Định nghĩa 10 (Remaining Utility) từ bài báo.
    """
    def __init__(self, tid: int, iutil: float, rutil: float):
        self.tid = tid
        self.iutil = iutil
        self.rutil = rutil

    def get_tid(self) -> int:
        return self.tid

    def get_iutil(self) -> float:
        return self.iutil

    def get_rutil(self) -> float:
        return self.rutil

    def __str__(self):
        return f"(tid={self.tid}, iutil={self.iutil:.2f}, rutil={self.rutil:.2f})"
