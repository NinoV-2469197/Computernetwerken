import subprocess
import multiprocessing
import time

# Check wether server simply replies to a single PING

def test_PING_1_output():
    # Run the script in the background
    p = subprocess.Popen(["python", "test/pang_server.py"])
    time.sleep(2) # Wait for it to open

    import socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    clientSocket.settimeout(3)

    address = ("localhost", 2000)

    clientSocket.sendto("PING-1!".encode(), address)
    dataGram = clientSocket.recvfrom(256)



    p.terminate()
    print(dataGram[0].decode())
    assert dataGram[0].decode() == "PONG-1!"

if __name__ == "__main__":
    test_PING_1_output()
