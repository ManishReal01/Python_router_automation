from netmiko import ConnectHandler

# Define the router configuration with hardcoded credentials
router = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.111',
    'username': 'cisco',
    'password': 'cisco123!',
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
        save_output = connection.save_config()
        print(f"Configuration saved:\n{save_output}")
    except Exception as e:
        print(f"Failed to add user: {e}")

def main():
    connection = connect_to_router(router)
    if connection is None:
        return
    
    new_user = input("Enter new username: ")
    new_password = input("Enter new password: ")
    add_user(connection, new_user, new_password)
    
    connection.disconnect()
    print("Disconnected from the router.")

if __name__ == "__main__":
    main()
