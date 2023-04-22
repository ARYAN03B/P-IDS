import socket

# Define the IP address and port to listen on
SERVER_IP = "192.168.0.100"
SERVER_PORT = 5000

# Create a socket connection to listen for client connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(1)

# Accept client connections and receive data
while True:
    client_socket, address = server_socket.accept()
    print(f"Connection from {address} established")

    # Receive data from the client
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        
        # Save the received data to a file
        with open("packet_data.txt", "a") as file:
            file.write(data + "\n")
    
    # Close the client socket connection
    client_socket.close()
