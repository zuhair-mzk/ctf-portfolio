import json

# Load the JSON data
with open('test.json', 'r') as file:
    data = json.load(file)

# Check which domains and protocols were used
for entry in data:
    print(f"Server: {entry['servername']}, Protocol: {entry['protocol']}")

# Identify unusual patterns or specific sequences
protocol_counts = {}
for entry in data:
    key = (entry['servername'], entry['protocol'])
    protocol_counts[key] = protocol_counts.get(key, 0) + 1

print("\nOccurrences by Server and Protocol:")
for key, count in protocol_counts.items():
    print(f"{key}: {count} times")