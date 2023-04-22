import socket
import pyshark
import netifaces

# Prompt the user for the IP address and port number of the server
SERVER_IP = input("Enter the server IP address: ")
SERVER_PORT = int(input("Enter the port: "))

# Get a list of all available network interfaces
interfaces = netifaces.interfaces()

# Filter out loopback and down interfaces
interfaces = [iface for iface in interfaces if "lo" not in iface and netifaces.ifaddresses(iface).get(netifaces.AF_INET)]

# Print the available interface names
print("Available interfaces:")
for iface in interfaces:
    print(iface)

# Prompt the user for the interface to capture packets on
interface = input("Enter the name of the interface to capture packets on: ")

# Create a socket connection to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

# Define the capture filter to capture only relevant packets
capture_filter = "tcp port 80"

# Start capturing packets
capture = pyshark.LiveCapture(interface=interface, display_filter=capture_filter)

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
    
# Send the packet details to the server
    client_socket.send(str(packet_details).encode())

# Close the socket connection
client_socket.close()

