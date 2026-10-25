import socket
import time

def measure_latency(host, port):
    start = time.perf_counter()
    
    try:
        with socket.create_connection(
            (host, port), timeout=3
        ):
            end = time.perf_counter()
            latency = (end - start) * 1000
            return latency
    except OSError:
        return None

def main():
    host = "example.com"
    port = 443
    
    print(f"monitoring {host}:{port}")
    print("Press Ctrl+C to stop.\n")
    
    try:
        while True:
            latency = measure_latency(host, port)
        
            if latency is not None:
                print(f"[OK] {latency:.2f} ms")
            else:
                print("[FAIL] Connection failed")
            
            time.sleep(1)            
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
        
if __name__ == "__main__":
    main()        
                    