import socket
import time
import csv
from datetime import datetime
from pathlib import Path

# 設定
HOST = "example.com"
PORT = 443
INTERVAL = 1

# プロジェクト直下のdataフォルダに保存
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CSV_FILE = DATA_DIR / "network_log.csv"

def measure_latency(host, port):
    start = time.perf_counter()
    
    try:
        with socket.create_connection(
            (host, port), timeout=3
        ):
            latency = (time.perf_counter() - start) * 1000
            return latency
        
    except OSError:
        return None

def save_result(timestamp, host, port, latency):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    #ファイルがまだ存在しない場合だけヘッダーを追加
    new_file = not CSV_FILE.exists() or CSV_FILE.stat().st_size == 0
    
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        if new_file:
            writer.writerow([
                "timestamp","host", "port", "status", "latency_ms"
            ])
            
        status = "OK" if latency is not None else "FAIL"
        
        writer.writerow([
            timestamp,
            host,
            port,
            status,
            f"{latency:.2f}" if latency is not None else ""
        ])    
def main():
    total = 0
    success = 0
    latency_sum = 0.0

    print(f"monitoring {HOST}:{PORT}")
    print("Press Ctrl+C to stop.\n")
    
    try:
        while True:
            timestamp = datetime.now().isoformat(timespec="seconds")
            latency = measure_latency(HOST, PORT)
        
            if latency is not None:
                success += 1
                latency_sum += latency
                print(f"[{timestamp}] [OK] {latency:.2f} ms")
            else:
                print(f"[{timestamp}] [FAIL] Connection failed")
            
            save_result(timestamp, HOST, PORT, latency)
            time.sleep(INTERVAL)            
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
    
    finally:
        print("\n=== Statidtics ===")
        print(f"Total measurements: {total}")
        
        if total > 0:
            print(f"Success rate: {success / total * 100:.1f}%") 
        
        if success > 0:
            print(f"Average latency: {latency_sum / success:.2f} ms")
            
        print(f"CSV saved to: {CSV_FILE}")           
        
if __name__ == "__main__":
    main()        
                    