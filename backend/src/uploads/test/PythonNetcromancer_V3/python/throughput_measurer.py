from mysql.connector import OperationalError as MySQLOperationalError
#from sqlLink import mydb, mycursor
from custom_logger import logger
import psutil
import time


import mysql.connector
#global mycursor
mydb = mysql.connector.connect(
  host="localhost",
  user="dbuser",
  password="vv2j@&T2zax@HhApm2",
  database="sqlinthesky"
)

mycursor = mydb.cursor()



def get_network_throughput(interval):
    # Get the initial values
    initial_bytes_sent = psutil.net_io_counters().bytes_sent
    initial_bytes_recv = psutil.net_io_counters().bytes_recv

    time.sleep(interval)

    # Get the final values after the specified interval
    final_bytes_sent = psutil.net_io_counters().bytes_sent
    final_bytes_recv = psutil.net_io_counters().bytes_recv

    # Calculate the throughput in bytes per second
    sent_throughput = final_bytes_sent - initial_bytes_sent
    recv_throughput = final_bytes_recv - initial_bytes_recv

    # Convert bytes to megabytes and calculate throughput in MB/s
    sent_throughput_mb = sent_throughput / (1024 * 1024 * interval)
    recv_throughput_mb = recv_throughput / (1024 * 1024 * interval)

    return sent_throughput_mb, recv_throughput_mb

def insertThroughput():
    interval = 0.1
    try:
        while True:
            sent_throughput, recv_throughput = get_network_throughput(interval)
            logger.info(f"Sent Throughput: {sent_throughput:.2f} MB/s | Recv Throughput: {recv_throughput:.2f} MB/s")
            sql = "INSERT INTO tblThroughput (dtTimestamp, dtIncoming, dtOutgoing) VALUES (NOW(), %s, %s)"
            val = (sent_throughput, recv_throughput)
            mycursor.execute(sql, val)
            mydb.commit()
            #time.sleep(2)
            #print(f"Sent Throughput: {sent_throughput}, Recieved Throughput: {recv_throughput}")
    except (Exception, MySQLOperationalError) as e:
            logger.warning(f"MySQL OperationalError: {type(e).__name__} - {e}")
            mydb.ping(reconnect=True)
            logger.error(f"Error in insertThroughput: {type(e).__name__} - {e}")
    finally:
         logger.info("Closing database connection")
         mydb.close()


#insertThroughput()
