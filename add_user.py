from netmiko import ConnectHandler
from getpass import getpass

# Router connection details
router = {
    'device_type': 'cisco_ios',
    'host': '127.0.0.1',  # Confirm this IP
    'username': 'admin',
    'password': 'admin',
    'port': 22,  # Confirm this port
}

# Debug: Print connection details
print(f"Attempting to connect to {router['host']} on port {router['port']}")

# User details to be added
new_user = {
    'username': 'new_user',
    'password': 'new_password',
}

# Connect to the router
try:
    connection = ConnectHandler(**router)
    print(f"Connected to {router['host']}")

    # Add a new user
    config_commands = [
        f"username {new_user['username']} password {new_user['password']}",
    ]
    output = connection.send_config_set(config_commands)
    print("User added successfully.")
    print(output)

    # Close the connection
    connection.disconnect()

except Exception as e:
    print(f"Failed to connect or execute commands: {e}")
