import subprocess
import multiprocessing
import time

# Check wether the server does not reply to bogus input
# Check wether the server is still running after bogus input

def test_PANG_output():
    # Run the script in the background
    p = subprocess.Popen(["python", "test/ping_server.py"])
    time.sleep(2) # Wait for it to open

    import socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    clientSocket.settimeout(3)

    address = ("localhost", 2000)

    try:
        clientSocket.sendto("PANG-1!".encode(), address)
        dataGram = clientSocket.recvfrom(256)
        assert False
    except TimeoutError:
        assert p.poll() == None
        assert p.returncode == None
        assert True
    finally:
        p.terminate()

    

