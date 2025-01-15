# packet_capture.py
#from sqlLink import mydb, mycursor
import pyshark
import time
from custom_logger import logger


import mysql.connector
#global mycursor
mydb = mysql.connector.connect(
  host="localhost",
  user="dbuser",
  password="vv2j@&T2zax@HhApm2",
  database="sqlinthesky"
)

mycursor = mydb.cursor()


avoid_destination_ips = ["192.168.178.84", "192.168.178.44","192.168.178.28", "10.0.97.99", "10.0.96.170"]  # Replace with the IP addresses you want to avoid
avoid_source_ips = ["192.168.178.84", "192.168.178.44", "192.168.178.28", "10.0.97.99", "10.0.96.170"]

def packet_callback(packet):
    try:
        if 'IP' in packet:
            src_ip = packet.ip.src
            dst_ip = packet.ip.dst

            # Check if the packet's destination IP is not in the list to avoid
            if dst_ip not in avoid_destination_ips and src_ip not in avoid_source_ips:
                logger.info(f"Incoming Packet: {src_ip} → {dst_ip}")
                sql = "INSERT INTO tblPacket (dtSrcIP, dtDestIP) VALUES (%s, %s)"
                val = (src_ip, dst_ip)
                print(f"Source IP: {src_ip}, Destination IP: {dst_ip}")
                mycursor.execute(sql, val)
                mydb.commit()
    except Exception as e:
        logger.error(f"Error in packet_callback: {type(e).__name__} - {e}")
        

def capture_packets(iface):
    while True:
        try:
            capture = pyshark.LiveCapture(interface=iface)
            capture.apply_on_packets(packet_callback)
            #time.sleep(2)
        except Exception as e:
            logger.error(f"Error in capture_packets: {type(e).__name__} - {e}")
        finally:
            # Close the database connection in a finally block
            logger.info("Closing database connection")
            mydb.close()

#capture_packets("enp0s8")