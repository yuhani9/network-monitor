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
    
    latency = measure_latency(host, port)
    
    if latency is not None:
        print(f"Connected: {host}:{port}")
        print(f"Latency: {latency:.2f} ms")
    else:
        print("Connection failed")
if __name__ == "__main__":
    main()        
                    