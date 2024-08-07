from netmiko import ConnectHandler
import sys

# Define the router configuration with Telnet and no credentials
router = {
    'device_type': 'cisco_ios_telnet',  # Use 'cisco_ios_telnet' for Telnet
    'ip': '172.20.20.3',  # Updated IP address
    'port': 5000,  # Port for Telnet connection
}

def connect_to_router(router):
    try:
        print("Connecting to router...")
        connection = ConnectHandler(**router)
        print("Successfully connected to router.")
        return connection
    except Exception as e:
        print(f"Failed to connect to the router: {e}")
        return None

def add_user(connection, new_user, new_password):
    try:
        print(f"Adding user {new_user}...")
        commands = [
            f"username {new_user} privilege 15 secret {new_password}"
        ]
        output = connection.send_config_set(commands)
        print(f"User {new_user} added:\n{output}")
        # Save the configuration
        save_output = connection.send_command('write memory')  # 'write memory' is used to save configuration in Telnet sessions
        print(f"Configuration saved:\n{save_output}")
    except Exception as e:
        print(f"Failed to add user: {e}")

def main(username, password):
    connection = connect_to_router(router)
    if connection is None:
        return
    
    new_user = username
    new_password = password
    add_user(connection, new_user, new_password)
    
    connection.disconnect()
    print("Disconnected from the router.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python router_automation_test.py <username> <password>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
