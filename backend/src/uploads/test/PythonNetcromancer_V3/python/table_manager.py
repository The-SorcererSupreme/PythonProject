# table_manager.py
# Import necessary packages
import socket
from custom_logger import logger
import mysql.connector

# Initialize MySQL connection and cursor
mydb = mysql.connector.connect(
    host="localhost",
    user="dbuser",
    password="vv2j@&T2zax@HhApm2",
    database="sqlinthesky"
)

mycursor = mydb.cursor()

def get_hostname(ip):
    try:
        # Get the hostname corresponding to the given IP address
        hostname = socket.gethostbyaddr(ip)
        return hostname[0]
    except socket.herror:
        return "Unknown"

def update_host_record(mac_address, new_hostname, new_ip):
    try:
        # Check if the MAC address exists in the table
        mycursor.execute("SELECT dtHostname, dtIP FROM tblHosts WHERE dtMAC = %s", (mac_address,))
        result = mycursor.fetchone()

        if result:
            current_hostname, current_ip = result

            # Use a conditional UPDATE query to update records
            mycursor.execute("""
                UPDATE tblHosts
                SET dtHostname = CASE
                    WHEN dtHostname = 'Unknown' AND %s != 'Unknown' THEN %s
                    WHEN dtHostname != %s THEN %s
                    ELSE dtHostname
                END,
                dtIP = CASE
                    WHEN dtIP != %s THEN %s
                    ELSE dtIP
                END,
                dtStatus = "Online"
                WHERE dtMAC = %s
            """, (new_hostname, new_hostname, new_hostname, new_hostname, new_ip, new_ip, mac_address))

            mydb.commit()
            print(f"Record updated for MAC address {mac_address}")
        else:
            # Insert a new record if the MAC address is not found
            mycursor.execute("""INSERT INTO tblHosts (dtHostname, dtIP, dtMAC) VALUES (%s, %s, %s)""", (new_hostname, new_ip, mac_address))
            mydb.commit()
            print(f"No record found for MAC address {mac_address}")

    except Exception as e:
        print(f"Error updating record: {type(e).__name__} - {e}")

def get_host_mac_addresses():
    try:
        # Retrieve all MAC addresses from tblHosts
        mycursor.execute("SELECT dtMAC FROM tblHosts")
        result = mycursor.fetchall()
        return [record[0] for record in result]
    except Exception as e:
        print(f"Error retrieving MAC addresses from tblHosts: {type(e).__name__} - {e}")
        return []

def update_host_status(mac_address, new_status):
    try:
        # Update the status of a host to "Offline"
        mycursor.execute("UPDATE tblHosts SET dtStatus = %s WHERE dtMAC = %s", (new_status, mac_address))
        mydb.commit()
        print(f"Status updated to {new_status} for MAC address {mac_address}")
    except Exception as e:
        print(f"Error updating status: {type(e).__name__} - {e}")

def update_table():
    try:
        # Read scan results from the file
        with open('/var/www/html/php/scan_results.txt', 'r') as file:
            scan_results = file.readlines()

        scanned_macs = []
        for line in scan_results:
            # Extract MAC address and IP address from the line
            parts = line.strip().split(' ')
            mac_address = parts[2]
            print(mac_address)
            ip_address = parts[-1]
            print(ip_address)
            scanned_macs.append(mac_address)
            
            # Resolve hostname
            hostname = get_hostname(ip_address)
            
            # Update or insert the host record in the database
            update_host_record(mac_address, hostname, ip_address)

        # Get all MAC addresses from tblHosts
        tblhosts_macs = get_host_mac_addresses()

        # Update status to "Offline" for MAC addresses in tblHosts but not in the scan results
        for mac_address in tblhosts_macs:
            if mac_address not in scanned_macs:
                update_host_status(mac_address, "Offline")

    except Exception as e:
        print(f"Error updating table: {type(e).__name__} - {e}")

update_table()