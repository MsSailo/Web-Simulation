# Description: This program is a client that connects to a web server and proxy server
#              and retrieves the html file, images, and scripts from the web server.
#              The program takes the following command-line arguments:
#              1. hostname of the web server
#              2. port number of the web server
#              3. path of the html file
#              4. hostname of the proxy server (optional)
#              5. port number of the proxy server (optional)
#              6. time in seconds for cache expiration (optional)
# Import the necessary libraries
import socket  # for socket programming
import ssl  # cannot connect to port 443 without ssl
import sys  # for command-line arguments
import os  # for object naming
from bs4 import BeautifulSoup  # for parsing html file

# global variables
folder_path = 'obj'


# function to retrieve the html file
def retrieve(hostname, port, path, proxy=None, proxy_port=None, sec=None):

    # create a socket object
    ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the server
    if proxy != None and proxy_port != None:
        ssocket.connect((proxy, proxy_port))
    else:
        ssocket.connect((hostname, port))

    # send the request
    if port == 443:
        request = f"GET {path} HTTP/1.0\r\nHost: {hostname}:{port}\r\n\r\n"
        if proxy == None:
            request = f"GET {path} HTTP/1.0\r\nHost:www.{hostname}\r\n\r\n"
            ssl_context = ssl.create_default_context()
            ssocket = ssl_context.wrap_socket(
                ssocket, server_hostname=hostname)
    else:  # port 80
        request = f"GET {path} HTTP/1.0\r\nHost: {hostname}:{port}\r\n\r\n"

    if sec != None:
        request = f"GET {path} HTTP/1.0\r\nHost: {hostname}:{port}\r\n\r\n{sec}"

    # send the request
    ssocket.send(request.encode())

    # Receive the response
    response = b''
    while True:
        # receive the data
        data = ssocket.recv(4096)
        if not data:
            break
        # append the data to the response
        response += data

    # close the socket
    ssocket.close()

    # split the response into header and body
    try:
        headers, body = response.split(b'\r\n\r\n', 1)
    except Exception as e:
        headers, body = response.split(b'DOCTYPE HTML', 1)
    except Exception as e:
        headers, body = response.split(b'DOCTYPE html', 1)

    # decode the header
    soup = BeautifulSoup(body, 'lxml')

    text = soup.get_text()  # get the text from the html file

    print(text)

    img_tags = soup.find_all('img')  # find all the image tags
    if len(img_tags) != 0:
        # for each image tag, get the image url and name
        for img in img_tags:
            img_url = img['src']
            img_name = os.path.basename(img_url)
            if proxy != None and proxy_port != None:
                img_get(hostname, port, img_url,
                        img_name, proxy, proxy_port, sec)
            else:
                img_get(hostname, port, img_url, img_name)
    else:
        print("No image found!!")

    js_tags = soup.find_all('script')  # find all the script tags
    if len(js_tags) != 0:
        # for each script tag, get the script url and name
        for js in js_tags:
            if 'src' in js.attrs:
                js_url = js['src']
                js_name = os.path.basename(js_url)
                if proxy != None and proxy_port != None:
                    js_get(hostname, port, js_url,
                           js_name, proxy, proxy_port, sec)
                else:
                    js_get(hostname, port, js_url, js_name)
    else:
        print("No script found!!")

# function to retrieve the image file


def img_get(hostname, port, url, name, proxy=None, proxy_port=None, sec=None):
    # create a socket object
    ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the proxy server
    if proxy != None and proxy_port != None:
        ssocket.connect((proxy, proxy_port))
        request = f'GET {url} HTTP/1.0\r\nHost: {hostname}:{port}\r\n\r\n'
    else:
        ssocket.connect((hostname, port))
        request = f'GET {url} HTTP/1.0\r\nHost: {hostname}:{port}\r\n\r\n'

    if port == 443 and proxy == None:
        ssl_context = ssl.create_default_context()
        ssocket = ssl_context.wrap_socket(ssocket, server_hostname=hostname)

    if sec != None:
        request = f'GET {url} HTTP/1.0\r\nHost: {hostname}:{port}\r\n\r\n{sec}'

    # send the request
    ssocket.send(request.encode())

    # Receive the response
    picture = b''

    while True:
        # receive the data
        data = ssocket.recv(4096)
        if len(data) < 1:
            break
        # append the data to the response
        picture = picture + data

    # close the socket
    ssocket.close()

    # Look for the end of the header (2 CRLF)
    pos = picture.find(b"\r\n\r\n")

    # Skip past the header and save the picture data
    picture = picture[pos+4:]
    name = hostname+name  # name the image file
    file_path = os.path.join(folder_path, name)  # create the file path
    with open(file_path, 'wb') as img_file:  # open the file
        img_file.write(picture)  # write the image data to the file
        print("Image saved.")  # print the message

# function to retrieve the script file


def js_get(hostname, port, url, name, proxy=None, proxy_port=None, sec=None):
    # create a socket object
    ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the proxy server
    if proxy != None and proxy_port != None:
        ssocket.connect((proxy, proxy_port))
        request = f'GET {url} HTTP/1.0\r\nHost: {hostname}:{port}\r\n\r\n'
    else:
        ssocket.connect((hostname, port))
        request = f'GET {url} HTTP/1.0\r\nHost: {hostname}:{port}\r\n\r\n'

    if port == 443 and proxy == None:
        ssl_context = ssl.create_default_context()
        ssocket = ssl_context.wrap_socket(ssocket, server_hostname=hostname)

    if sec != None:
        request = f'GET {url} HTTP/1.0\r\nHost: {hostname}:{port}\r\n\r\n{sec}'

    # send the request
    ssocket.send(request.encode())

    # Receive the response
    script = b''

    while True:
        # receive the data
        data = ssocket.recv(4096)
        if len(data) < 1:
            break
        # append the data to the response
        script = script + data

    # close the socket
    ssocket.close()

    name = hostname+name  # name the script file
    file_path = os.path.join(folder_path, name)  # create the file path
    with open(file_path, 'wb') as js_file:  # open the file
        js_file.write(script)  # write the script data to the file
        print("JS saved.")  # print the message

# Driver (main) function


def main():
    # check the number of command-line arguments
    if len(sys.argv) == 4:
        hostname = sys.argv[1]
        port = int(sys.argv[2])
        path = sys.argv[3]
        retrieve(hostname, port, path)

    elif len(sys.argv) == 6:
        hostname = sys.argv[1]
        port = int(sys.argv[2])
        path = sys.argv[3]
        proxy = sys.argv[4]
        proxy_port = int(sys.argv[5])
        retrieve(hostname, port, path, proxy, proxy_port)

    elif len(sys.argv) == 7:
        hostname = sys.argv[1]
        port = int(sys.argv[2])
        path = sys.argv[3]
        proxy = sys.argv[4]
        proxy_port = int(sys.argv[5])
        time = sys.argv[6]
        retrieve(hostname, port, path, proxy, proxy_port, time)

    else:
        print("Invalid choice!!")


# call the main function
if __name__ == "__main__":
    main()
