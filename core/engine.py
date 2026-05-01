import lz4.frame

class VantageEngine:
    """
    VANTAGE V-AI CORE ENGINE v4.0.0
    Kiến trúc Stateless LZ4 Stream tối ưu hóa bộ nhớ và băng thông CPU.
    """
    def __init__(self, batch_size=25000):
        self.vault = []
        self.batch_size = batch_size

    def fast_commit_batch(self, batch_data_bytes):
        """
        Nén và lưu trữ dữ liệu theo khối (Batch) để tận dụng L1/L2 Cache.
        """
        compressed = lz4.frame.compress(batch_data_bytes)
        self.vault.append(compressed)
        return len(compressed)

    def get_vault_size(self):
        """Trả về tổng dung lượng dữ liệu đã nén trong RAM (Bytes)"""
        return sum(len(b) for b in self.vault)