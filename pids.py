import socket
import pyshark
import json
import os
import time

# Prompt the user for the IP address and port number of the server
SERVER_IP = input("Enter the server IP address: ")
SERVER_PORT = int(input("Enter the server port number: "))

# Define the path to store the captured packets
packet_dir = "./packets"

# Create a socket connection to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

# Get a list of all interfaces on the machine
import netifaces
interfaces = netifaces.interfaces()

# Get a list of available interfaces
available_interfaces = []
for iface in interfaces:
    try:
        pyshark.get_interface(iface)
        available_interfaces.append(iface)
    except:
        pass

# Ask the user to select an interface to capture packets on
print("Available interfaces:")
for i in range(len(available_interfaces)):
    print(f"{i+1}. {available_interfaces[i]}")
iface_index = int(input("Select an interface to capture packets on: ")) - 1
iface = available_interfaces[iface_index]

# Start capturing packets on the selected interface
capture = pyshark.LiveCapture(interface=iface)

# Create the packet directory if it doesn't exist
if not os.path.exists(packet_dir):
    os.makedirs(packet_dir)

# Loop through the captured packets and extract relevant characteristics
for packet in capture.sniff_continuously():
    packet_details = {
        "src_ip": packet.ip.src,
        "dst_ip": packet.ip.dst,
        "src_port": packet.tcp.srcport,
        "dst_port": packet.tcp.dstport,
        "payload": packet.tcp.payload,
        "protocol": packet.transport_layer,
        "length": packet.length,
        "timestamp": packet.sniff_time
    }

    # Write the packet details to a file
    file_name = f"{packet_dir}/{packet_details['timestamp']}.json"
    with open(file_name, "w") as f:
        json.dump(packet_details, f)

    # Send the packet details to the server
    client_socket.send(json.dumps(packet_details).encode())

# Close the socket connection
client_socket.close()

# Analyze the captured packets
dangerous_protocols = ["TCP", "UDP"]
packet_files = os.listdir(packet_dir)
for file_name in packet_files:
    with open(f"{packet_dir}/{file_name}", "r") as f:
        packet_details = json.load(f)
        if packet_details["protocol"] in dangerous_protocols:
            print(f"WARNING: {file_name} contains a potentially dangerous packet!")
