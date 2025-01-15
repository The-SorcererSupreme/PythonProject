import sys
import signal
import threading
import time
from network_scanner_final import scan
from traffic_analyser import capture_packets
from throughput_measurer import insertThroughput
from ARP_sniffer import main
from table_manager import update_table

def scan_and_update(network_range, stop_event):
    while not stop_event.is_set():
        # Clear the scan_results.txt file before starting the scan
        open('/var/www/html/php/scan_results.txt', 'w').close()
        
        scan(network_range)
        time.sleep(20)  # Sleep for 10 seconds before the next scan
        update_table()

        # Add a sleep interval between scans if needed

def signal_handler(sig, frame):
    print("Ctrl+C detected! Stopping threads...")
    stop_event.set()

# Create a stop event
stop_event = threading.Event()

# Setup signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Start the ARP sniffer thread with the stop event
arp_sniffer = threading.Thread(target=main, args=(stop_event,))
arp_sniffer.start()

# Start the scan thread which will start update_table after scan completes
scan_thread = threading.Thread(target=scan_and_update, args=('192.168.178.0/24', stop_event))
scan_thread.start()

# Start the capture packets and measure throughput threads
capturePackets_thread = threading.Thread(target=capture_packets, args=('enp0s3',))
measureThroughput_thread = threading.Thread(target=insertThroughput)

capturePackets_thread.start()
measureThroughput_thread.start()

# Join the threads to wait for their completion if necessary
# (though you might not want to join arp_sniffer if it's meant to run indefinitely)
capturePackets_thread.join()
measureThroughput_thread.join()
scan_thread.join()

# Optionally join arp_sniffer if you want to wait for it to stop
arp_sniffer.join()
