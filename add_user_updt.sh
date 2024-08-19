#!/bin/bash

# Define the Python script content
PYTHON_SCRIPT=$(cat <<EOF
import paramiko
import time
import os

def run_ssh_commands(commands):
    host = "127.0.0.1"
    port = 22
    username = "admin"
    password = "admin"

    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the router
        ssh.connect(host, port, username, password)

        # Start an interactive shell session
        shell = ssh.invoke_shell()

        # Run the commands
        for command in commands:
            if command:  # Only send non-empty commands
                shell.send(f"{command}\n")
                time.sleep(1)

        # Read the output from the shell
        output = shell.recv(10000).decode('utf-8')
        print(output)

    except paramiko.AuthenticationException:
        print("Authentication failed.")
    except paramiko.SSHException as e:
        print(f"SSH error: {e}")
    finally:
        # Close the SSH connection
        ssh.close()

def main():
    hostname = os.getenv('HOSTNAME', '').strip()  # Get hostname from environment variable
    new_user = os.getenv('NEW_USER', '').strip()  # Get new username from environment variable
    new_password = os.getenv('NEW_PASSWORD', '').strip()  # Get new password from environment variable

    commands = []

    if hostname:
        commands.append(f"hostname {hostname}")  # Set the hostname if provided

    if new_user and new_password:
        commands.append(f"username {new_user} privilege 15 password {new_password}")  # Add new user if both username and password are provided

    commands.extend(["end", "write memory"])  # Exit configuration mode and save

    run_ssh_commands(commands)

if __name__ == "__main__":
    main()

EOF
)

# Step 1: Create the Python script inside the container
sudo docker exec -i -u root clab-firstlab-csr-r1 bash -c "echo '$PYTHON_SCRIPT' > /root/add_user.py"

# Step 2: Install Paramiko if it's not already installed
sudo docker exec -i -u root clab-firstlab-csr-r1 bash -c "pip3 install paramiko"

# Step 3: Run the Python script inside the container
sudo docker exec -i -u root clab-firstlab-csr-r1 bash -c "HOSTNAME=\$HOSTNAME NEW_USER=\$NEW_USER NEW_PASSWORD=\$NEW_PASSWORD python3 /root/add_user.py"
