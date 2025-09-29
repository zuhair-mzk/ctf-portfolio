#!/usr/local/bin/python3

import json
from scapy.all import *

load_layer('http')
load_layer('tls')
load_layer('dns')

results = []

# =============================================
# ========= write your code below  ============
# =============================================

def packet_filter(packet):
    # DNS Queries
    if packet.haslayer(DNS) and packet.haslayer(UDP):
        if packet[UDP].dport == 53:
            qr = packet['DNS Question Record']
            if qr.qtype == 1:
                return True
    # HTTP Requests
    if packet.haslayer(TCP):
        if packet[TCP].dport == 80:
            if packet.haslayer(HTTPRequest):
                return True
    # HTTPS Requests (TLS Client Hello)
        elif packet[TCP].dport == 443:
            if packet.haslayer(TLS) and packet.haslayer(TLS_Ext_ServerName):
                return True
    return False


def packet_process(packet):
    sip = packet[IPv6].src if (IPv6 in packet) else packet[IP].src
    dip = packet[IPv6].dst if (IPv6 in packet) else packet[IP].dst

    # DNS
    if packet.haslayer(DNS) and packet.haslayer(UDP) and packet[UDP].dport == 53:
        qr = packet['DNS Question Record']
        if qr.qtype == 1:
            servername = packet[DNS].qd.qname.decode("utf-8").rstrip('.')
            record = {
                "src": sip,
                "dst": dip,
                "protocol": "DNS",
                "servername": servername
            }
            results.append(record)
            print(f"Captured DNS request: {record}")
            return

    # HTTP
    if packet.haslayer(TCP) and packet[TCP].dport == 80 and packet.haslayer(HTTPRequest):
        http_layer = packet[HTTPRequest]
        host = http_layer.Host.decode() if http_layer.Host else "unknown"
        record = {
            "src": sip,
            "dst": dip,
            "protocol": "HTTP",
            "servername": host
        }
        results.append(record)
        print(f"Captured HTTP request: {record}")
        return

    # HTTPS
    if packet.haslayer(TCP) and packet[TCP].dport == 443:
        if packet.haslayer(TLS) and packet.haslayer(TLS_Ext_ServerName):
            tls_layer = packet[TLS_Ext_ServerName]
            if tls_layer.servernames:
                servername = tls_layer.servernames[0].servername.decode()
            else:
                servername = "unknown"
            record = {
                "src": sip,
                "dst": dip,
                "protocol": "HTTPS",
                "servername": servername
            }
            results.append(record)
            print(f"Captured HTTPS request: {record}")
            return



# =============================================
# ===== do not modify the code below ==========
# =============================================
    
def run(count, filepath):
    sniff(iface="eth0", lfilter=packet_filter, prn=packet_process, count=count)
    with open(filepath, "w") as file_stream:
        file_stream.write(json.dumps(results, indent=4))
    
if __name__ == "__main__":
    import os, sys, getopt
    def usage():
       print ('Usage:	' + os.path.basename(__file__) + ' filepath ')
       print ('\t -c count, --count=count')
       sys.exit(2)
    # extract parameters
    try:
         opts, args = getopt.getopt(sys.argv[1:],"hc:",["help", "count="])
    except getopt.GetoptError as err:
         print(err)
         usage()
         sys.exit(2)
    count = None
    filepath = args[0] if len(args) > 0 else None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
           usage()
        elif opt in ("-c", "--count"):
           try:
                count = int(arg)
           except ValueError:
                print("count must be a natural number")
                sys.exit(2)
    if (count is None):
        print('count option is missing\n')
        usage()
    if (filepath is None):
        print('filepath is missing\n')
        usage()
    # run the command
    run(count, filepath)