# Client code
import socket

# Define the host and port to connect to
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

# Create a TCP/IP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # Connect to the server
    client_socket.connect((HOST, PORT))
    
    # Communication loop
    while True:
        # Send data to the server
        message = input("Enter a message to send: ")
        if message.lower() == 'exit':
            break  # Break the loop to close the connection
        client_socket.sendall(message.encode())

        # Receive data from the server
        data = client_socket.recv(1024)
        if not data:
            break  # No data means the server has closed the connection

        print(f"Received from server: {data.decode()}")