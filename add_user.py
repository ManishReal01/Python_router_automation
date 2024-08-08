import sys
from netmiko import ConnectHandler

if len(sys.argv) != 4:
    print("Usage: python3 add_user.py <HOSTNAME> <NEW_USERNAME> <NEW_PASSWORD>")
    sys.exit(1)

hostname = sys.argv[1]
new_username = sys.argv[2]
new_password = sys.argv[3]

device = {
    'device_type': 'cisco_ios',
    'host': hostname,
    'username': 'your_existing_username',  # Replace with actual username
    'password': 'your_existing_password',  # Replace with actual password
    'secret': 'your_enable_password',      # Replace with actual enable password, if any
    'conn_timeout': 20,                    # Increase connection timeout
}

try:
    connection = ConnectHandler(**device)
    connection.enable()

    commands = [
        f"username {new_username} privilege 15 secret {new_password}"
    ]
    output = connection.send_config_set(commands)
    print(output)

    connection.disconnect()
except Exception as e:
    print(f"Failed to connect or execute commands: {e}")
