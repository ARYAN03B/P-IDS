import netifaces
import pyshark

# Get a list of available network interfaces
interfaces = netifaces.interfaces()

# Print out the list of interfaces to the user
print("Available network interfaces:")
for i, interface in enumerate(interfaces):
    print(f"{i+1}. {interface}")

# Prompt the user to select an interface
selection = input("Enter the number of the interface you would like to use: ")

# Convert the user input to an integer and subtract 1 to get the index of the selected interface
interface_index = int(selection) - 1

# Get the name of the selected interface
interface_name = interfaces[interface_index]
interface = interface_name

# Create a capture object to capture live packets on the interface
capture = pyshark.LiveCapture(interface)

# Get a list of available network interfaces
interfaces = netifaces.interfaces()# Loop through the captured packets and extract relevant characteristics
for packet in capture.sniff_continuously():
    packet_details = {
        "src_ip": packet.ip.src,
        "dst_ip": packet.ip.dst,
        "protocol": packet.transport_layer,
        "length": packet.length,
        "timestamp": packet.sniff_time
    }

# Loop through the captured packets and print their details
for packet in capture:
    print(packet)
