import sys
import paramiko

def authenticate_ssh(username, password):
    try:
        # Establish SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('127.0.0.1', username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command('hostname')
        hostname = stdout.read().strip().decode('utf-8')
        # Authentication successful
        ssh.close()
        print("Authentication successful! Access granted.")
        print(f"Hostname: {hostname}")
        sys.exit(0)

    except Exception as e:
        # Authentication failed
        print(f"Authentication failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python authenticate_user.py <username> <password>")
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]

    # Call the authentication function
    authenticate_ssh(username, password)
