import socket
from scapy.all import IP, sniff, Raw, send, conf
import sys
import mysql.connector
from mysql.connector import Error

def find_available_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('127.0.0.1', 0))  # Bind to any available port on localhost
        return s.getsockname()[1]  # Get the assigned port

def get_latest_request(session_id):
    try:
        connection = mysql.connector.connect(
            host='your_database_host',
            database='your_database_name',
            user='your_database_user',
            password='your_database_password'
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute(f"SELECT idRequest FROM tblRequest WHERE sessionId = '{session_id}' ORDER BY timestamp DESC LIMIT 1")
            request = cursor.fetchone()
            return request['idRequest'] if request else None
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def update_request_status(request_id, status, port):
    try:
        connection = mysql.connector.connect(
            host='your_database_host',
            database='your_database_name',
            user='your_database_user',
            password='your_database_password'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(f"UPDATE tblRequest SET dtStatus = '{status}', dtSocket = {port} WHERE idRequest = {request_id}")
            connection.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Set the network interface to monitor mode (replace 'enp0s8' with your interface)
conf.iface = 'enp0s3'

# Assume sys.argv[1] is the user session ID
session_id = sys.argv[1]

# Create a socket for communication
port = find_available_port()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', port))
server_socket.listen(1)

print(f"Waiting for connection on port {port}...")

try:
    # Add an entry to tblRequest
    connection = mysql.connector.connect(
        host='your_database_host',
        database='your_database_name',
        user='your_database_user',
        password='your_database_password'
    )
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO tblRequest (sessionId, timestamp, dtStatus) VALUES ('{session_id}', NOW(), 'waiting')")
        connection.commit()

    # Wait for the connection from the PHP script
    client_socket, client_address = server_socket.accept()
    print(f"Connected to {client_address}")

    # Get the latest request ID for the user session
    request_id = get_latest_request(session_id)

    # Update the request status to 'connected' and provide the port
    update_request_status(request_id, 'connected', port)

    # Send a signal to PHP script indicating readiness to receive new payload
    client_socket.send("READY".encode())

    # Read the new payload from PHP script
    new_payload = client_socket.recv(1024).decode()

    # Start sniffing and apply the packet_callback function
    sniff(prn=lambda x: packet_callback(x, nmask, proto, new_payload), store=0)

except KeyboardInterrupt:
    print("\nCapturing interrupted by user.")
finally:
    # Close the sockets
    server_socket.close()
    if 'client_socket' in locals():
        client_socket.close()
    if connection.is_connected():
        cursor.close()
        connection.close()
