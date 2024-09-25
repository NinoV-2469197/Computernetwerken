import socket
import time
import sys


def calculate_average(numbers):
    if not numbers:
        return 0

    total_sum = sum(numbers)
    count = len(numbers)
    average = total_sum / count
    return average


# Provide default values for SERVER_ADDR and SERVER_PORT
SERVER_ADDR = sys.argv[1] if len(sys.argv) > 1 else "localhost"
SERVER_PORT = 2000

# Number of pings to send
PING_COUNT = int(sys.argv[2]) if len(sys.argv) > 2 else 4

# Timeout in seconds for each ping response
TIMEOUT = 1


def main():
    # 1. Socket Creation: We create a UDP socket using socket.socket(socket.AF_INET, socket.SOCK_DGRAM). UDP is connectionless, so you don't need to establish a connection before sending the data.
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2. Timeout Handling: client_socket.settimeout(TIMEOUT) sets a timeout for blocking socket operations. If no response is received within this time, a socket.timeout exception is triggered.
    client_socket.settimeout(TIMEOUT)

    RTTs = []
    TIMEOUTS = 0
    STARTTIMES = []

    # 3. Sending and Receiving Messages: The sendto method sends data to the server, and recvfrom waits to receive data from the server. The server's response should be a "pong" message.
    for seq in range(0, PING_COUNT):
        # 4. Timing: We're using time.time() to record the time before sending the message. On receiving a response, we compute the round-trip time by subtracting the start time from the current time.
        STARTTIMES.append(time.time())
        message = f"PING-{seq}!"
        try:
            # Send the ping message to the server
            client_socket.sendto(message.encode(), (SERVER_ADDR, SERVER_PORT))
            # Wait for the pong reply
            data, server = client_socket.recvfrom(1024)
            current_time = time.time()
            rtt = int((current_time - STARTTIMES[seq])*1000)
            RTTs.append(rtt)
            print(f"{data.decode()[5:-1]}: {rtt}ms")
        except socket.error as e:
            print(f"Socket error: {e}")
        except socket.timeout:
            TIMEOUTS += 1
            print(f"{seq}: timeout")

    print(f"AVG={calculate_average(RTTs)}ms TIMEOUTS={TIMEOUTS}")

    # Close the socket
    client_socket.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
