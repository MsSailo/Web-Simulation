# Description: A simple HTTP server that serves files from the web directory
# Import the necessary libraries
import socket  # for socket operations
import threading  # for threading operations
import os  # for file operations

# Define the server's IP address and port
SERVER_HOST = '0.0.0.0'  # Listen on all available network interfaces
SERVER_PORT = 8080  # Choose an available port

# Define the path to the directory where your HTML files are stored
WEB_ROOT = 'web'


# Create a function to handle client requests
def handle_client(client_socket):
    # Receive the client request data
    request = client_socket.recv(4096).decode()
    request_lines = request.split('\r\n')

    # Parse the HTTP request
    if len(request_lines) > 0:
        request_line = request_lines[0].split()
        if len(request_line) > 1:
            method = request_line[0]
            path = request_line[1]

            # Determine the file path on the server
            file_path = os.path.join(WEB_ROOT, path[1:])

            # Check if the file exists
            if method == 'GET':
                try:
                    with open(file_path, 'rb') as file:
                        response = file.read()
                        client_socket.send(b'HTTP/1.1 200 OK\r\n\r\n')
                        client_socket.send(response)
                except FileNotFoundError:
                    # File not found, send a 404 response
                    client_socket.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
                    client_socket.send(b'404 Not Found')
    client_socket.close()


# Create the main server socket and start listening for incoming connections
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_HOST, SERVER_PORT))
server.listen(5)  # Listen for up to 5 incoming connections
print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

# Start the infinite loop to begin accepting client connections
while True:
    client_socket, addr = server.accept()
    print(f"Accepted connection from {addr[0]}:{addr[1]}")

    # Create a thread to handle the client request
    client_handler = threading.Thread(
        target=handle_client, args=(client_socket,))
    client_handler.start()
