from checkClient import checkClient

# Given bogus responses -->
# Check wether the client returns normal output
# Check wether the client returns no errors
# TODO: Check wether the client calculates proper AVG (WONTFIX: 3rd bachelor students are assumed to know how to calculate an average)

N_PINGS = 10

def test_ping_client_3():
    checkClient("test/bogus_server.py", "ping_client.py", N_PINGS)

if __name__ == '__main__':
    test_ping_client_3()
