#!/bin/bash

ROUTER_HOST=$1
ROUTER_USERNAME=$2
ROUTER_PASSWORD=$3
NEW_HOSTNAME=$4
INTERFACE=$5
INTERFACE_IP=$6
SUBNET_MASK=$7
DEFAULT_GATEWAY=$8
MOTD_BANNER=$9
NEW_USER=${10}
NEW_USER_PASSWORD=${11}

# Define the Python script content with parameter checks
PYTHON_SCRIPT=$(cat <<EOF
import paramiko
import time

def run_ssh_commands(commands):
    host = "$ROUTER_HOST"
    port = 22
    username = "$ROUTER_USERNAME"
    password = "$ROUTER_PASSWORD"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, port, username, password)
        shell = ssh.invoke_shell()

        for command in commands:
            shell.send(f"{command}\\n")
            time.sleep(1)

        output = shell.recv(10000).decode('utf-8')
        print(output)

    except paramiko.AuthenticationException:
        print("Authentication failed.")
    except paramiko.SSHException as e:
        print(f"SSH error: {e}")
    finally:
        ssh.close()

def main():
    commands = ["enable", "configure terminal"]

    if "$NEW_HOSTNAME":
        commands.append(f"hostname $NEW_HOSTNAME")

    if "$INTERFACE" and "$INTERFACE_IP" and "$SUBNET_MASK":
        commands.append(f"interface $INTERFACE")
        commands.append(f"ip address $INTERFACE_IP $SUBNET_MASK")
        commands.append("no shutdown")
        commands.append("exit")

    if "$DEFAULT_GATEWAY":
        commands.append(f"ip route 0.0.0.0 0.0.0.0 $DEFAULT_GATEWAY")

    if "$MOTD_BANNER":
        commands.append(f"banner motd #$MOTD_BANNER#")

    if "$NEW_USER" and "$NEW_USER_PASSWORD":
        commands.append(f"username $NEW_USER privilege 15 secret $NEW_USER_PASSWORD")

    commands.append("write memory")

    # Capture and save the running configuration
    commands.append("show running-config")

    run_ssh_commands(commands)

if __name__ == "__main__":
    main()
EOF
)

# Step 1: Create the Python script inside the container
sudo docker exec -i -u root clab-firstlab-csr-r1 bash -c "echo '$PYTHON_SCRIPT' > /root/router.py"

# Step 2: Install Paramiko if it's not already installed
sudo docker exec -i -u root clab-firstlab-csr-r1 bash -c "pip3 install paramiko"

# Step 3: Run the Python script inside the container and save the running config
sudo docker exec -i -u root clab-firstlab-csr-r1 bash -c "python3 /root/router.py > /root/running_config.txt"

# Optional: Copy the running configuration to the host system (if required)
sudo docker cp clab-firstlab-csr-r1:/root/running_config.txt .
