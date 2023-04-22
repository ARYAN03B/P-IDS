import os

# Define the path to the file containing the packet data
file_path = "packet_data.txt"

# Read the packet data from the file
with open(file_path, "r") as file:
    packet_data = file.readlines()

# Loop through the packet data and analyze each packet
for packet in packet_data:
    # Extract relevant characteristics from the packet data
    packet = eval(packet) # Convert the string representation of the dictionary to a dictionary object
    src_ip = packet["src_ip"]
    dst_ip = packet["dst_ip"]
    src_port = packet["src_port"]
    dst_port = packet["dst_port"]
    protocol = packet["protocol"]
    payload = packet["payload"]
    length = packet["length"]
    
    # Perform analysis on the packet characteristics to detect suspicious activity
    # For example, you could check for large amounts of data being transmitted, connections to known malicious IP addresses, or unusual patterns of traffic.
    # Here's an example of checking for connections to a known malicious IP address:
    if dst_ip == "192.168.0.50":
        print(f"Suspicious connection detected from {src_ip} to {dst_ip}")
    
# Remove the file containing the packet data to prevent it from growing too large
os.remove(file_path)
