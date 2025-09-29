#!/usr/local/bin/python3

import sys
from urllib.parse import urlparse, parse_qs, quote
import http.client
import hlextend

# =============================================
# ========= write your code below  ============
# =============================================
def attack(url):
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    
    # Extract the student ID and the tag
    student_id = query_params['sid'][0]
    tag = query_params['tag'][0]

    # Load the fake HMAC
    with open('fake-hmac.txt', 'rb') as f:
        fake_hmac = f.read()

    # Construct the new URL to set the mark to 100
    new_url = f"https://grades.seclab.space/?tag={tag}&sid={student_id}&mark=100"

    # Send the request to set the mark
    http_conn = http.client.HTTPSConnection(parsed.hostname)
    http_conn.request("GET", new_url)
    response = http_conn.getresponse()

    # Output the status and the new URL
    print(f"Response Status: {response.status}")
    print(f"Response Body: {response.read().decode('utf-8')}")  # Print the response body
    print(new_url)  # Print the constructed URL to verify

    return new_url  # Return the new URL for further verification

# =============================================
# ===== do not modify the code below ==========
# =============================================
            
if __name__ == "__main__":
   import os, sys, getopt
   def usage():
        print ('Usage:    ' + os.path.basename(__file__) + ' url ')
        sys.exit(2)
   try:
      opts, args = getopt.getopt(sys.argv[1:],"h",["help"])
   except getopt.GetoptError as err:
      print(err)
      usage()
   # extract parameters
   url = args[0] if len(args) > 0 else None
   # check arguments
   if (url is None):
       print('url is missing\n')
       usage()
   # run the command
   print(attack(url))