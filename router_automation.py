from netmiko import ConnectHandler
from datetime import datetime
import os

# Define the router configuration
router = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.111',
    'username': os.getenv('ROUTER_USERNAME'),
    'password': os.getenv('ROUTER_PASSWORD'),
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

def backup_router_config(connection):
    try:
        print("Backing up configuration...")
        running_config = connection.send_command("show running-config")
        current_dir = os.getcwd()
        backup_filename = os.path.join(current_dir, f"backup_{router['ip']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(backup_filename, 'w') as backup_file:
            backup_file.write(running_config)
        print(f"Configuration backup saved to {backup_filename}")
    except Exception as e:
        print(f"Failed to backup configuration: {e}")

def monitor_interfaces(connection):
    try:
        print("Monitoring interfaces...")
        output = connection.send_command('show ip interface brief')
        print(f"Interface status:\n{output}")
    except Exception as e:
        print(f"Failed to monitor interfaces: {e}")

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

def monitor_bandwidth(connection):
    try:
        print("Monitoring bandwidth...")
        output = connection.send_command('show interfaces')
        print(f"Bandwidth usage:\n{output}")
    except Exception as e:
        print(f"Failed to monitor bandwidth: {e}")

def upgrade_firmware(connection, image_name):
    try:
        print(f"Upgrading firmware to {image_name}...")
        commands = [
            f"copy tftp://<tftp_server_ip>/{image_name} flash:",
            f"boot system flash:{image_name}",
            "write memory",
            "reload"
        ]
        output = connection.send_config_set(commands)
        print(f"Firmware upgrade output:\n{output}")
    except Exception as e:
        print(f"Failed to upgrade firmware: {e}")

def run_diagnostics(connection):
    try:
        print("Running diagnostics...")
        commands = [
            'show ip route',
            'show log',
            'show processes cpu',
            'show processes memory'
        ]
        for command in commands:
            output = connection.send_command(command)
            print(f"Output of '{command}':\n{output}\n")
    except Exception as e:
        print(f"Failed to run diagnostics: {e}")

def setup_basic_security(connection):
    try:
        print("Setting up basic security functions...")
        commands = [
            # Enable SSH
            "ip domain-name example.com",
            "crypto key generate rsa modulus 1024",
            "ip ssh version 2",
            "line vty 0 4",
            "transport input ssh",
            "login local",
            "exit",

            # Enable AAA
            "aaa new-model",
            "aaa authentication login default local",
            "aaa authorization exec default local",

            # Configure enable secret
            "enable secret 0 myenablepassword",

            # Set up a basic firewall
            "access-list 100 permit tcp any any eq 22",
            "access-list 100 permit tcp any any eq 23",
            "access-list 100 permit icmp any any",
            "access-list 100 deny ip any any",
            "interface GigabitEthernet0/0",
            "ip access-group 100 in",
            "exit",
            "write memory"
        ]
        output = connection.send_config_set(commands)
        print(f"Basic security setup output:\n{output}")
    except Exception as e:
        print(f"Failed to set up basic security: {e}")

def main():
    connection = connect_to_router(router)
    if connection is None:
        return
    
    while True:
        print("\nRouter Automation Script")
        print("1. Backup Configuration")
        print("2. Monitor Interfaces")
        print("3. Add User")
        print("4. Monitor Bandwidth")
        print("5. Upgrade Firmware")
        print("6. Run Diagnostics")
        print("7. Set Up Basic Security")
        print("8. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            backup_router_config(connection)
        elif choice == '2':
            monitor_interfaces(connection)
        elif choice == '3':
            new_user = input("Enter new username: ")
            new_password = input("Enter new password: ")
            add_user(connection, new_user, new_password)
        elif choice == '4':
            monitor_bandwidth(connection)
        elif choice == '5':
            image_name = input("Enter the name of the new firmware image: ")
            upgrade_firmware(connection, image_name)
        elif choice == '6':
            run_diagnostics(connection)
        elif choice == '7':
            setup_basic_security(connection)
        elif choice == '8':
            connection.disconnect()
            print("Disconnected from the router.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
