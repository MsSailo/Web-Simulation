# Description: A simple web proxy server with caching functionality
# Import the necessary libraries
import socket  # for socket operations
import threading  # for threading operations
import ssl  # for SSL operations
import os  # for file operations

# for time operations
import datetime
import pytz


# Define the proxy server's IP address and port
PROXY_HOST = ''
PROXY_PORT = 8881

dir_path = 'cache'


# Create a function to handle client requests
def handle_cache(client_socket):
    # Receive data from the client
    request = client_socket.recv(4096)
    print(f"REQUEST:\n{request}\n\n\n")

    sec = 0

    # Parse the client request
    client_request = request.decode()
    client_request = client_request.split('\r\n')

    if client_request[3]:
        sec = client_request[3]
        print(f"Sec: {sec}\n")

    print(f'SEC: {sec}')

    # Parse the file path from the request
    request_file_path = client_request[0].split(' ')[1]

    if request_file_path == '/':
        file_name = "index.html"
    else:
        file_name = request_file_path.split('/')[-1]
    print(f'Name: {file_name}\n')

    # Get the destination host and port
    host = [header for header in client_request if header.startswith("Host:")]
    host = host[0].split(' ')

    try:
        dest_host = host[1].split(':')[0]
        print(f'Dest Host: {dest_host}')
        dest_port = int(host[1].split(':')[1])
    except Exception as e:
        dest_host = host[1]
        dest_port = 80  # default port for HTTP

    file_name = dest_host+file_name  # file name with host name
    file_path = os.path.join(dir_path, file_name)  # file path with host name

    print(f"File Path: {file_path}\n\n")

    # Check if the file exists
    if os.path.exists(file_path):
        print(f"The file '{file_name}' exists in folder '{dir_path}'.")

        # Check if the file is expired
        expire_path = '.expire'
        expire_path = file_path+expire_path

        # If the file is expired, fetch the file from the server
        if os.path.exists(expire_path):
            with open(expire_path, 'rb') as obj_file:
                expire = obj_file.read()
                expire = expire.decode()

                expire = expire.split(' ')
                time = expire[3].split(':')

                print(f'{expire[0]}\t{time[0]}\t{time[1]}\t{time[2]}')
                day = int(expire[0])*86400
                hour = int(time[0])*3600
                minute = int(time[1])*60
                second = int(time[2])

                expire_time = day + hour + minute + second

                # Get the current time in GMT/UTC
                gmt = pytz.utc.localize(datetime.datetime.utcnow())

                # Format the GMT time as a string
                formatted_gmt = gmt.strftime("%d %H %M %S")

                local_time = formatted_gmt.split(' ')
                local_day = int(local_time[0])*86400
                local_hour = int(local_time[1])*3600
                local_minute = int(local_time[2])*60
                local_second = int(local_time[3])

                total_local_time = local_day + local_hour + local_minute + local_second

                time_path = '.time'
                time_path = file_path+time_path

                total_saved_time = 0

                with open(time_path, 'rb') as obj_file:
                    saved_time = obj_file.read()
                    saved_time = saved_time.decode()
                    saved_time = saved_time.split(' ')
                    saved_day = int(saved_time[0])*86400
                    saved_hour = int(saved_time[1])*3600
                    saved_minute = int(saved_time[2])*60
                    saved_second = int(saved_time[3])

                    total_saved_time = saved_day + saved_hour + saved_minute + saved_second

                if sec != 0:
                    if total_local_time < expire_time and total_local_time < total_saved_time+int(sec):
                        with open(file_path, 'rb') as obj_file:
                            data = obj_file.read()

                            client_socket.send(data)

                            client_socket.close()

                            print("Connection Closed.\n\n")
                    else:
                        fetch(client_request, dest_host,
                              dest_port, file_path, request)
                elif sec == 0:
                    if total_local_time < expire_time:
                        with open(file_path, 'rb') as obj_file:
                            data = obj_file.read()

                            client_socket.send(data)

                            client_socket.close()

                            print("Connection Closed with sec 0\n\n")
                    else:
                        fetch(client_request, dest_host,
                              dest_port, file_path, request)

                else:
                    print("ERROR")

        else:
            print(
                f"The file '{expire_path}' does not exist in folder '{dir_path}'.")

            fetch(client_request, dest_host, dest_port, file_path, request)

    else:
        print(f"The file '{file_name}' does not exist in folder '{dir_path}'.")

        fetch(client_request, dest_host, dest_port, file_path, request)


# Create a function to fetch the file from the server
def fetch(client_request, dest_host, dest_port, file_path, request):

    print(f'Client Request: {client_request}\n\n')

    print(f'Host: {dest_host}\t\tPort: {dest_port}\n\n')

    # Create a socket to connect to the remote server
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    remote_socket.connect((dest_host, dest_port))

    if dest_port == 443:
        path = client_request[0].split(' ')[1]
        print(path)
        request = f"GET {path} HTTP/1.0\r\nHost:www.{dest_host}\r\n\r\n"
        request = request.encode()
        ssl_context = ssl.create_default_context()
        remote_socket = ssl_context.wrap_socket(
            remote_socket, server_hostname=dest_host)

    # Send the client request to the remote server
    remote_socket.send(request)

    # Receive the response
    t_data = b''

    # Relay data between client and remote server
    while True:
        data = remote_socket.recv(4096)
        if len(data) == 0:
            break
        client_socket.send(data)

        t_data += data

    # Create the cache folder if it does not exist
    with open(file_path, 'wb') as obj_file:
        obj_file.write(t_data)
        print("Cached.")

    # split the response into header and body
    headers, body = t_data.split(b'\r\n\r\n', 1)
    headers = headers.decode()
    headers = headers.split('\r\n')

    # Get the expiration date of the file from the response header and save it
    expires = [header for header in headers if header.startswith("Expires:")]

    try:
        expire_txt = expires[0].split(', ')[1]
        expire_txt = expire_txt.encode()
        expire_path = '.expire'
        expire_path = file_path+expire_path

        with open(expire_path, 'wb') as obj_file:
            obj_file.write(expire_txt)
            print("Cached.")

        gmt = pytz.utc.localize(datetime.datetime.utcnow())

        # Format the GMT time as a string
        formatted_gmt = gmt.strftime("%d %H %M %S")
        formatted_gmt = formatted_gmt.encode()
        time_path = '.time'
        time_path = file_path+time_path

        with open(time_path, 'wb') as obj_file:
            obj_file.write(formatted_gmt)
            print("Time Saved.")

    except Exception as e:
        pass

    remote_socket.close()
    client_socket.close()
    print("Connection CLOSED!!\n\n")


# Create the proxy server socket
proxy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_server.bind((PROXY_HOST, PROXY_PORT))
proxy_server.listen(5)
print(f"Proxy server listening on {PROXY_HOST}:{PROXY_PORT}")

# Start the infinite loop to begin accepting client connections
while True:
    client_socket, addr = proxy_server.accept()
    print(f"Accepted connection from {addr[0]}:{addr[1]}")

    # Create a thread to handle the client request
    client_handler = threading.Thread(
        target=handle_cache, args=(client_socket,))
    client_handler.start()
