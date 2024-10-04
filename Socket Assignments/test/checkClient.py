import re
import subprocess
import time

# Take the started processe
def checkClient(server_name, client_name, N_PINGS):

    p = subprocess.Popen(["python", server_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2) # Wait for it to open

    c = subprocess.Popen(["python", client_name, "localhost", str(N_PINGS)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2) # Wait for it to open

    c.wait()
    
    p.terminate()
    p_outs, p_errs = p.communicate()
    c_outs, c_errs = c.communicate()

    assert c_errs == b'', "Error occured in client code: {error}".format(error=c_errs)

    s_lengths = re.findall(r'(\d+)', p_outs.decode('utf-8')) # Parse artificially delayed times from server output
    c_lengths = re.findall(r'(\d+)ms| (timeout)', c_outs.decode('utf-8')) # Parse reported RTTs from client output

    c_timeouts_reported = re.findall(r'TIMEOUTS=(\d+)', c_outs.decode('utf-8')) # Parse timeouts counted from client output


    c_timeouts = 0 # Count server reported times > 1000 (would lead to a timeout)
    s_timeouts = 0 # Count client reported timeouts in output


    for i in range(N_PINGS):
        if int(s_lengths[i]) >= 1000:
            s_lengths[i] = "timeout"
            s_timeouts += 1


    

    # Check wether for every transmitted PING wether the reported value is equal to the expected value
    for i in range(N_PINGS):
        if c_lengths[i][0] == "":
            assert c_lengths[i][1] == s_lengths[i], "Report error! output: {} expected: {}".format(c_lengths[i][1], s_lengths[i])
            c_timeouts += 1
        else:
            assert int(s_lengths[i])-5 < int(c_lengths[i][0]) < int(s_lengths[i])+5, "Report error output was much different from expected value! output: {} expected: {}".format(c_lengths[i][0], s_lengths[i])



    assert int(c_timeouts_reported[0]) == c_timeouts and  s_timeouts == c_timeouts, "Timeouts reported and calculated do not match!"


