#!/usr/bin/env python3

import socket
import sys
import random
from pyfiglet import Figlet

# Define a function to print usage instructions
def print_usage():
    print("Usage: port_scan.py [-v] [-s]")
    print("Options:")
    print("  -v  Print the script version.")
    print("  -s  Perform a service version scan.")

# Define the script version
script_version = "1.1"

# Define color codes
RED = "\033[91m"
BLACK = "\033[30m"
GREEN = "\033[92m"
RESET = "\033[0m"

# Define a list of motivational messages
motivational_messages = [
    "Ready to pwn the box and find those flags!",
    "Stay sharp and keep your tools honed.",
    "May your exploits be as smooth as a zero-day.",
    "Remember, with great power comes great responsibility.",
    "Hack the planet, one port at a time!",
]

# Function to get a random motivational message
def get_motivational_message():
    return random.choice(motivational_messages)

# Define a function to perform the port scan
def port_scan(target_host, start_port, end_port, service_scan=False):
    for port in range(start_port, end_port + 1):
        # Create a socket object
        sock = create_socket()
        
        # Attempt to connect to the target host and port
        result = connect_to_target(sock, target_host, port)
        
        # Check the result and report if the port is open or closed
        if result == "open":
            print(GREEN + f"Port {port} is open" + RESET)
            if service_scan:
                service_version = get_service_version(target_host, port)
                if service_version:
                    print(BLACK + f"   Service version: {service_version}" + RESET)
        else:
            print(RED + f"Port {port} is closed" + RESET)

# Define a function to create a socket
def create_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock

# Define a function to connect to the target host and port
def connect_to_target(sock, target_host, port):
    try:
        # Set a timeout for the connection attempt
        sock.settimeout(1)
        
        # Attempt to connect to the target host and port
        sock.connect((target_host, port))
        
        # If successful, the port is open
        return "open"
    except Exception as e:
        # If an error occurs, the port is closed
        return "closed"
    finally:
        # Close the socket
        sock.close()

# Define a function to get service version information
def get_service_version(target_host, port):
    try:
        # Create a socket object
        sock = create_socket()
        
        # Set a timeout for the connection attempt
        sock.settimeout(2)
        
        # Attempt to connect to the target host and port
        sock.connect((target_host, port))
        
        # Receive up to 1024 bytes of data from the service
        banner = sock.recv(1024).decode('utf-8').strip()
        
        return banner
    except Exception as e:
        return None
    finally:
        sock.close()

# Main program
if __name__ == "__main__":
    # Create a custom font object
    custom_font = Figlet(font='slant')
    
    # Generate the ASCII art for "simple scanner"
    ascii_art = custom_font.renderText('Simple Scanner')
    
    # Print the ASCII art in green color
    print(GREEN + ascii_art + RESET)
    
    # Print initial messages in black and red
    print(BLACK + "A Simple Port Scanner Tool!" + RESET)
    print(RED + "Created by Chad Nelson" + RESET)
    
    # Display a random motivational message
    print(get_motivational_message())
    
    # Check for command line flags
    if len(sys.argv) > 1:
        if "-v" in sys.argv:
            print(f"Port Scan Script Version {script_version}")
            sys.exit()
        if "-s" in sys.argv:
            service_scan = True
        else:
            service_scan = False
    else:
        service_scan = False

    target_host = input("Enter the target host IP address: ")
    start_port = int(input("Enter the start port: "))
    end_port = int(input("Enter the end port: "))
    
    print(f"Scanning {target_host} from port {start_port} to {end_port}...")
    
    # Perform the port scan
    port_scan(target_host, start_port, end_port, service_scan)
