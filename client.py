import socket

# Server address and port must match the server script
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000

# Create a UDP socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Message to send distance
message = "distance"

try:
    # Send the request to the server
    client.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

    # Receive the response from the server
    data, _ = client.recvfrom(1024)  # buffer size is 1024 bytes
    print("Received distance from server:", data.decode())

except Exception as e:
    print("An error occurred:", e)

finally:
    client.close()