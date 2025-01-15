# network_scanner_final.py
from scapy.all import ARP, Ether, srp
import multiprocessing
from ipaddress import ip_network
from concurrent.futures import ThreadPoolExecutor
import threading
import time

def arp_scan(ip):
    try:
        print(f"Scanning {ip}...")
        arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
        srp(arp_request, timeout=1, verbose=0, iface='enp0s3')
    except Exception as e:
        print(f"Error scanning IP {ip}: {type(e).__name__} - {e}")

def worker(ip_subset):
    with ThreadPoolExecutor(max_workers=65536) as executor:
        futures = [executor.submit(arp_scan, ip) for ip in ip_subset]
        for future in futures:
            future.result()

def scan(subnet):

    # Split the subnet into individual IP addresses
    ip_list = [str(ip) for ip in ip_network(subnet).hosts()]
    num_processes = 32
    chunk_size = len(ip_list) // num_processes

    # Create a list to hold the processes
    processes = []

    start_time = time.time()  # Start the timer
    
    # Create and start processes
    for i in range(num_processes):
        ip_subset = ip_list[i * chunk_size: (i + 1) * chunk_size]
        process = multiprocessing.Process(target=worker, args=(ip_subset,))
        process.start()
        processes.append(process)
    
    # If there are remaining IPs, handle them in the main process
    if len(ip_list) % num_processes != 0:
        remaining_ips = ip_list[num_processes * chunk_size:]
        worker(remaining_ips)

    try:
        # Wait for all processes to finish
        for process in processes:
            process.join()

        end_time = time.time()  # End the timer
        elapsed_time = end_time - start_time
        print(f"Scan completed in {elapsed_time:.2f} seconds")
        # Wait 10 seconds
        # Stop sniffer
        # Start table update
        #

    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Exiting...")
        for process in processes:
            process.terminate()
        for process in processes:
            process.join()
        print("All processes terminated. Exiting gracefully.")