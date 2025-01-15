import os
from scapy.all import sniff, ARP

def load_known_arp_replies(file_path):
    known_replies = set()
    try:
        with open(file_path, "r") as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 4:
                    mac_address = parts[2]
                    known_replies.add(mac_address)
    except FileNotFoundError:
        pass  # If the file does not exist, start with an empty set
    return known_replies

def process_packet(packet, file_handle, known_replies):
    if ARP in packet and packet[ARP].op == 2:  # Check if the packet is an ARP reply
        mac_address = packet[ARP].hwsrc
        if mac_address not in known_replies:
            # Format the ARP reply details
            arp_reply = f"ARP Reply: {packet[ARP].hwsrc} is at {packet[ARP].psrc}\n"
            
            # Print to console (optional)
            print(arp_reply.strip())
            
            # Append to file
            file_handle.write(arp_reply)
            file_handle.flush()  # Ensure the write is immediate
            
            # Add to known replies to avoid duplicates
            known_replies.add(mac_address)

def main():
    # Set the network interface you want to capture packets from
    interface = "enp0s3"  # Replace with your network interface (e.g., eth0, wlan0)
    
    # Path to the results file
    results_dir = "/var/www/html/php"
    results_file = os.path.join(results_dir, "scan_results.txt")

    # Ensure the directory exists
    os.makedirs(results_dir, exist_ok=True)

    print(f"Capturing ARP reply packets on interface {interface}...")

    # Load known ARP replies to avoid duplicates
    known_replies = load_known_arp_replies(results_file)

    # Open the file in append mode
    with open(results_file, "a") as f:
        try:
            # Start sniffing on the specified interface for ARP packets
            sniff(iface=interface, filter="arp", prn=lambda x: process_packet(x, f, known_replies), store=False)

        except KeyboardInterrupt:
            print("\nCapture stopped.")

if __name__ == "__main__":
    main()
