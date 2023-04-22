import netifaces

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
