import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = BASE_DIR / "data" / "network_log.csv"
OUTPUT_DIR = BASE_DIR / "output"

def analyze_network():
    if not CSV_FILE.exists():
        print("CSV file not found.")
        return
    
    # CSV を読みこむ
    df = pd.read_csv(CSV_FILE)
    
    if df.empty:
        print("No measurement data.")
        return
    
    # 日時をdatetime型に変換
    df["timestamp"] = pd.to_datetime(
        df["timestamp"], errors="coerce"
    )
    
    # 応答時間を数値に変換
    df["latency_ms"] = pd.to_numeric(
        df["latency_ms"], errors="coerce"
    )
    
    #正常に測定されたデータだけを抽出
    success = df[
        (df["status"] == "OK")
        & df["timestamp"].notna()
        & df["latency_ms"].notna()
    ].copy()
    
    total = len(df)
    success_count = len(success)
    success_rate = success_count / total * 100
    
    print("=== Network Analysis ===")
    print(f"Total measurements: {total}")
    print(f"Success rate: {success_rate:.2f}%")
    
    if success.empty:
        print("No successful measurements.")
        return
    
    mean_latency = success["latency_ms"].mean()
    max_latency = success["latency_ms"].max()
    min_latency = success["latency_ms"].min()
    
    print(f"Average latency: {mean_latency:.2f} ms")
    print(f"Maximum latency: {max_latency:.2f} ms")
    print(f"Minimum latency: {min_latency:.2f} ms")
    
    # グラフ作成
    fig, ax = plt.subplots(figsize=(12,5))
    
    ax.plot(
        success["timestamp"],
        success["latency_ms"],
        label="TCP Connection Time"
    )
    
    ax.axhline(
        mean_latency,
        linestyle="--",
        label=f"Average: {mean_latency:.2f} ms"
    )
    
    ax.set_title("Network Latency Monitor")
    ax.set_xlabel("Time")
    ax.set_ylabel("Latency (ms)")
    ax.grid(True)
    ax.legend()
    
    fig.autofmt_xdate()
    fig.tight_layout()
    
    # PNGで保存
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / "latency_graph.png"
    
    fig.savefig(output_file, dpi=150)
    
    print(f"Graph saved to: {output_file}")
    
    plt.show()
    
if __name__ == "__main__":
    analyze_network()    