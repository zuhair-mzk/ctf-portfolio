import hashlib

# Read the secret key
with open('key.txt', 'rb') as key_file:
    key = key_file.read().strip()

# Define the URL parameters
sid = "[STUDENT_ID]"
url_params = f"sid={sid}"

# Generate the tag
tag = hashlib.sha256(key + url_params.encode()).hexdigest()

print(f"Generated Tag: {tag}")
