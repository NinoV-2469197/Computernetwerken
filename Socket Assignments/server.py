# Server code
import socket

# Define the host and port for the server
HOST = '127.0.0.1'  # Localhost, you can also use socket.gethostname() for the local IP
PORT = 65432        # Port to listen on (non-privileged ports > 1023)

# Create a TCP/IP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Bind the socket to the address and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen()

    print(f'Server listening on {HOST}:{PORT}...')

    # Accept the connection from a client
    conn, addr = server_socket.accept()
    with conn:
        print(f'Connected by {addr}')
        
        # Communication loop
        while True:
            # Receive data from the client
            data = conn.recv(1024)  # Receive up to 1024 bytes
            if not data:
                break  # No data means the client has closed the connection

            print(f"Received from client: {data.decode()}")

            # Send data back to the client (echo)
            response = input("Enter a message to send: ")
            conn.sendall(response.encode())