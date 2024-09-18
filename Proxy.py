# Description: A simple HTTP proxy server
# Import the necessary libraries
import socket  # for socket operations
import threading  # for threading operations
import ssl  # for SSL operations

# Define the proxy server's IP address and port
PROXY_HOST = ''
PROXY_PORT = 8882


# Function to handle client requests
def handle_client(client_socket):
    # Receive data from the client
    request = client_socket.recv(4096)
    print(f"REQUEST:\n{request}\n\n\n")

    # Parse the client request
    client_request = request.decode()
    client_request = client_request.split('\r\n')

    # Get the destination host and port
    host = [header for header in client_request if header.startswith("Host:")]
    print(host)
    host = host[0].split(' ')
    print(host)
    try:
        dest_host = host[1].split(':')[0]
        print(f'Dest Host: {dest_host}')
        dest_port = int(host[1].split(':')[1])
    except Exception as e:
        dest_host = host[1]
        dest_port = 80

    # Print the client request
    print(f'Client Request: {client_request}\n\n')

    # Print the destination host and port
    print(f'Host: {dest_host}\t\tPort: {dest_port}\n\n')

    # Create a socket to connect to the remote server
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    remote_socket.connect((dest_host, dest_port))

    # Send the client request to the remote server
    if dest_port == 443:
        path = client_request[0].split(' ')[1]
        print(path)
        request = f"GET {path} HTTP/1.0\r\nHost:www.{dest_host}\r\n\r\n"
        request = request.encode()
        ssl_context = ssl.create_default_context()
        remote_socket = ssl_context.wrap_socket(
            remote_socket, server_hostname=dest_host)

    remote_socket.send(request)

    # Relay data between client and remote server
    while True:
        data = remote_socket.recv(4096)
        if len(data) == 0:
            break
        client_socket.send(data)

    # Close the sockets
    remote_socket.close()
    client_socket.close()
    print("Connection CLOSED!!\n\n")


# Create the proxy server socket
proxy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_server.bind((PROXY_HOST, PROXY_PORT))
proxy_server.listen(5)
print(f"Proxy server listening on {PROXY_HOST}:{PROXY_PORT}")

# Continuously listen for client connections
while True:
    client_socket, addr = proxy_server.accept()
    print(f"Accepted connection from {addr[0]}:{addr[1]}")

    # Create a thread to handle the request from the client
    client_handler = threading.Thread(
        target=handle_client, args=(client_socket,))
    client_handler.start()
