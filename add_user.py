from netmiko import ConnectHandler
from getpass import getpass

# Router connection details
router = {
    'device_type': 'cisco_ios',  # Update as needed based on your router's type
    'host': '172.0.0.1',
    'username': 'admin',
    'password': 'admin',
    'port': 22,
}

# User details to be added
new_user = {
    'username': 'new_user',  # Update this to the new user's username
    'password': 'new_password',  # Update this to the new user's password
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
