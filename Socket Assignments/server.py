import socket
import re
import sys

# Server address and port
SERVER_ADDR = "localhost"  # Localhost to test locally
SERVER_PORT = 2000
BUFFERSIZE = 1024
PREFIX = "PONG-"


def makePongMsg(data):
    if data[:5] == "PING-" and data[-1] == '!':
        return PREFIX+data[5:-1]+'!'


def main():
    # A UDP socket is created using socket.socket(socket.AF_INET, socket.SOCK_DGRAM).
    # The socket is bound to a specific IP address and port with bind().
    # Listening for Messages:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the socket to the server address and port
        server_socket.bind((SERVER_ADDR, SERVER_PORT))
        server_socket.setblocking(False)

        print(f"Server listening on {SERVER_ADDR}:{SERVER_PORT}")

        # Communication loop
        while True:
            try:
                # Wait for a datagram from the client
                # The server uses recvfrom() to listen for incoming messages.
                # The server can receive data from any client, which is why the client's address is also captured.
                message, client_address = server_socket.recvfrom(BUFFERSIZE)
                # Upon receiving a message, the server decodes it and typically responds with a "pong" message, reflecting the sequence number back to the client.
                data = message.decode("utf-8")
                if data and makePongMsg(data):
                    print(f"Received: {data} from {client_address}")
                    # The sendto() function sends the response back to the client using the client's address.
                    server_socket.sendto(makePongMsg(
                        data).encode(), client_address)
                    print(f"Sent: {makePongMsg(data)} to {client_address}")
            except BlockingIOError:
                # No data available to read: loop back and continue to check for keyboard interrupt
                continue
            except socket.error as e:
                print(f"Socket error: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
            except KeyboardInterrupt:
                print("\nServer is shutting down.")
                break
        # Close the socket
        server_socket.close()


if __name__ == "__main__":
    try:
        main()
    # The server listens indefinitely, but you can stop it with a KeyboardInterrupt (e.g., pressing Ctrl+C in the terminal), which is caught to shut down the server gracefully.
    except KeyboardInterrupt:
        sys.exit(1)
