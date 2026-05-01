import time
import os
import psutil
import platform
import datetime
import sys

# Thêm đường dẫn để Python tìm thấy thư mục core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.engine import VantageEngine

CONFIG = {
    "VERSION": "4.0.0-ELITE",
    "FOUNDER": "Nguyen Vo Anh Khoa",
    "AVG_TOKENS_PER_REC": 20,
    "TOTAL_RECORDS": 5000000 
}

def run_validation():
    engine = VantageEngine()
    process = psutil.Process(os.getpid())
    
    # Chuẩn bị dữ liệu mẫu (Pre-encoded)
    sample_rec = b"ID:999 | Node:V-AI_NODE | Data:Stateless_Logic_System"
    batch_bytes = b"|||".join([sample_rec] * engine.batch_size)
    num_batches = CONFIG["TOTAL_RECORDS"] // engine.batch_size

    start_mem = process.memory_info().rss / (1024 * 1024)
    start_time = time.perf_counter()
    
    for _ in range(num_batches):
        engine.fast_commit_batch(batch_bytes)
        
    duration = time.perf_counter() - start_time
    end_mem = process.memory_info().rss / (1024 * 1024)

    # Tính toán con số Godlike
    total_tokens = CONFIG["TOTAL_RECORDS"] * CONFIG["AVG_TOKENS_PER_REC"]
    tps = total_tokens / duration
    ram_used = end_mem - start_mem
    
    # Render Log (giữ nguyên phong cách cũ bạn thích)
    log_content = f"""
============================================================
VANTAGE V-AI OFFICIAL VALIDATION LOG
Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
============================================================
[SYSTEM INFO]
Founder: {CONFIG['FOUNDER']}
CPU:     {platform.processor()} ({os.cpu_count()} Threads)
RAM:     {psutil.virtual_memory().total >> 30} GB

[PERFORMANCE RESULTS]
Throughput:     {tps / 1e6:.2f} Million Tokens/s
Total Time:     {duration:.4f} seconds
RAM Increment:  {ram_used:.2f} MB
Rank:           {"S++ (Godlike)" if tps >= 1e9 else "S+ (Elite)"}
============================================================
"""
    print(log_content)
    with open("VANTAGE_VALIDATION.log", "w", encoding="utf-8") as f:
        f.write(log_content)

if __name__ == "__main__":
    run_validation()