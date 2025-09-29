#!/usr/local/bin/python3

import json
from scapy.all import *
from urllib.parse import urlparse, parse_qs

load_layer('http')
load_layer('tls')
load_layer('dns')

results = []

# =============================================
# ========= write your code below  ============
# =============================================

def packet_filter(packet):
    return packet.haslayer('HTTPRequest') or packet.haslayer('HTTPResponse')


def packet_process(packet):
    if packet.haslayer('HTTPRequest'):
        # Handle HTTP request packet
        request = packet['HTTPRequest']
        host = request.Host.decode() if request.Host else None
        path = request.Path.decode() if request.Path else None
        method = request.Method.decode() if request.Method else None
        query_args = parse_qs(urlparse(path).query)
        cookies = request.Cookie.decode() if request.Cookie else None
        body = packet['Raw'].load.decode() if packet.haslayer('Raw') else None
        
        # Add to results
        results.append({
            "type": "request",
            "host": host,
            "method": method,
            "path": path,
            "query_args": query_args,
            "cookies": cookies,
            "body": body
        })

    elif packet.haslayer('HTTPResponse'):
        # Handle HTTP response packet
        response = packet['HTTPResponse']
        status_code = response.Status_Code.decode() if response.Status_Code else None
        cookies = response.Set_Cookie.decode() if response.Set_Cookie else None
        body = packet['Raw'].load.decode() if packet.haslayer('Raw') else None
        
        # Add to results
        results.append({
            "type": "response",
            "status_code": status_code,
            "cookies": cookies,
            "body": body
        })



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