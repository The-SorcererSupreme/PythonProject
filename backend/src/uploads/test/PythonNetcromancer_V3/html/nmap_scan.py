import nmap
import sys
import threading
import time
import json

def perform_nmap_scan(target_ip, start_port, end_port, result_list):
    nm = nmap.PortScanner()
    port_range = f"{start_port}-{end_port}"

    nm.scan(target_ip, arguments=f'-Pn -p {port_range} -T5')  # Scan the specified port range

    if target_ip in nm.all_hosts() and 'tcp' in nm[target_ip]:
        open_ports = [port for port in nm[target_ip]['tcp'] if nm[target_ip]['tcp'][port]['state'] == 'open']
        result_list.extend(open_ports)

def scan_port_range(target_ip, start_port, end_port, result_list):
    perform_nmap_scan(target_ip, start_port, end_port, result_list)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python nmap.py <target_ip>")
        sys.exit(1)

    target_ip = sys.argv[1]
    result_list = []

    # Define the port ranges you want to scan concurrently
    port_ranges = [(1, 1024), (1025, 2048), (2049, 3072)]

    # Start measuring execution time
    start_time = time.time()

    # Create threads for every 16 ports within each range
    threads = []
    for start_port, end_port in port_ranges:
        for port_chunk_start in range(start_port, end_port, 64):
            port_chunk_end = min(port_chunk_start + 63, end_port)
            thread = threading.Thread(target=scan_port_range, args=(target_ip, port_chunk_start, port_chunk_end, result_list))
            threads.append(thread)
            thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Stop measuring execution time
    end_time = time.time()

    # Print the consolidated results and execution time
    print(json.dumps(result_list))
    #print(f"Open ports on {target_ip}: {result_list}")
    #print(f"Total execution time: {end_time - start_time:.2f} seconds")
    #print(result_list)
