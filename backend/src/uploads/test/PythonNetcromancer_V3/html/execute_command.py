#!/usr/bin/env python3
import cgi
import paramiko

# Function to establish SSH connection
def establish_ssh_connection(username, password, hostname):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh_client.connect(hostname, username=username, password=password)
        return ssh_client
    except paramiko.AuthenticationException as auth_err:
        print(f"Authentication error: {auth_err}")
    except paramiko.SSHException as ssh_err:
        print(f"SSH connection error: {ssh_err}")
    except Exception as e:
        print(f"Error: {e}")
    
    return None

# Function to execute command on SSH session
def execute_ssh_command(ssh_client, command):
    if ssh_client:
        try:
            stdin, stdout, stderr = ssh_client.exec_command(command)
            return stdout.read().decode('utf-8')
        except Exception as e:
            print(f"Command execution error: {e}")
    
    return None

# Main CGI script handling
print("Content-type: text/plain\n")

form = cgi.FieldStorage()
command = form.getvalue("command")
username = form.getvalue("username")
password = form.getvalue("password")

if command and username and password:
    # Establish SSH connection
    ssh_client = establish_ssh_connection(username, password, '127.0.0.1')

    if ssh_client:
        # Execute command on SSH session
        output = execute_ssh_command(ssh_client, command)
        if output:
            print(output)

        # Close SSH connection
        ssh_client.close()
    else:
        print("SSH connection could not be established")
else:
    print("No command, username, or password provided")