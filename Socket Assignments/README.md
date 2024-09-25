
# Network Programming Guidelines

## Overview

This document provides guidelines and requirements for implementing a network socket program that handles multiple connections and errors gracefully. The program should set up a server socket using IPv4 and manage socket options such as reuse address to handle the TIME_WAIT state efficiently.

## Requirements

1. **Function Implementations:**
   - Implement `sent()` and `sentall()` functions to handle sending data over the network efficiently.

2. **Error Handling:**
   - Ensure all operations handle errors gracefully. Check for conditions such as connection failures, timeouts, and unexpected disconnections.

3. **Multiple Connections:**
   - Support handling multiple connections and sockets concurrently.

4. **Server Socket Setup:**
   - Setup a server socket to listen for incoming connections.
   - Use the IPv4 protocol.

5. **Socket Options:**
   - Enable the reuse address option to handle situations where sockets are in a `TIME_WAIT` state.

6. **Data Buffers:**
   - Use appropriate buffering techniques. Avoid using `recv(1)` for receiving data as it is inefficient.

7. **Network Byte Order:**
   - Use `socket.htons()` and `socket.ntohs()` to ensure data is in the correct network byte order.

8. **Testing:**
   - Use Wireshark to test and debug network communications. (Note: Wireshark is for testing only by the developer.)

## Implementation Details

### Socket Setup and Configuration

- **Address Family:** Use `socket.AF_INET` for IPv4.
- **Socket Type:** Use `socket.SOCK_STREAM` for TCP connections.

```python
import socket

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set socket options
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to an address and port
server_socket.bind(('localhost', 12345))

# Listen for incoming connections
server_socket.listen(5)
```

### Function Implementations

#### `sent()`

- Send data over a socket and handle partial sends.
  
```python
def sent(sock, data):
    total_sent = 0
    while total_sent < len(data):
        sent = sock.send(data[total_sent:])
        if sent == 0:
            raise RuntimeError("Socket connection broken")
        total_sent += sent
```

#### `sentall()`

- Continue sending data until the entire message is sent.
  
```python
def sentall(sock, data):
    sock.sendall(data)
```

### Error Handling

- Use try-except blocks to capture and handle various socket exceptions such as `socket.error` and `socket.timeout`.

```python
try:
    # Accept connections and handle them
    conn, addr = server_socket.accept()
    with conn:
        print('Connected by', addr)
        # Handle communication
except socket.error as e:
    print(f"Socket error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

### Data Reception and Byte Order

- Use buffered receive methods and always maintain network byte order for data transmission.

```python
buffer_size = 2048
data = conn.recv(buffer_size)
# Process data in a loop if expecting more
```

### Testing with Wireshark

- Use Wireshark to capture and analyze packets sent to and from the server to ensure correct implementation.

> **Note:** Wireshark setup is specific to the developer's testing environment.

By following these guidelines, you will create a robust network application capable of handling multiple connections, managing data efficiently, and gracefully handling errors. Ensure thorough testing using tools like Wireshark to verify correctness.
