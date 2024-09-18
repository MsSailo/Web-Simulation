# Web-Simulation

# Advanced Computer Networks Programming Assignment 2: WWW

This assignment encompasses four distinct parts. Part-1 entails the development of a web
client capable of connecting directly to web servers or via an intermediary web proxy using
TCP connections. The client sends HTTP requests, predominantly utilizing the GET method,
and displays server responses, supporting variable command line arguments for specifying
connection details. The Part-2 focuses on the creation of a web proxy, which connects to both
clients and servers, forwarding HTTP requests and responses. Parts 3 and 4 revolve around
the implementation of a multi-threaded web server, equipped to concurrently handle multiple
HTTP requests from clients, browsers, and web proxies. The server listens on a fixed port,
establishes separate threads for each request/response pair, processes incoming HTTP
requests, retrieves requested files, constructs HTTP responses, and dispatches them to clients.
In cases of missing files, the server issues an HTTP "404 Not Found" message. Threading is
employed for efficient parallel request management across all sections.

## Contents in the zip

1. Codes - Client.py, Server.py, Proxy.py, ExtendedProxy.py
2. Folders - web (contains a html file for server), obj (for saving images or scripts)
3. Report pdf and this Readme file


## Run Locally 

Install Python Dependencies

```bash
  pip3 install bs4 lxml
```

#### 1. Running the Server

```bash
  python3 Server.py
```

#### 2. Running the Proxy Server

```bash
  python3 Proxy.py
```

#### 3. Running the Extended Proxy

```bash
  python3 ExtendedProxy.py
```

#### 4. Running the Client

Port Number can be 80/443 or else the specified Port Number of Server.

a. For base file
```bash
  python3 Client.py <server url/ipaddress> <portnumber> /
```
b. For specific file
```bash
  python3 Client.py <server url/ipaddress> <portnumber> /<filename.extension>
```
c. For proxy (The <filename.extension> is optional here)
```bash
  python3 Client.py <server url/ipaddress> <server portnumber> /<filename.extension> <proxy ipaddress> <proxy portnumber>
```
d. For extended proxy (The <filename.extension> is optional here)
```bash
  python3 Client.py <server url/ipaddress> <server portnumber> /<filename.extension> <extendedproxy ipaddress> <extendedproxy portnumber>
```
e. For extended proxy with timeout (The <filename.extension> is optional here)
```bash
  python3 Client.py <server url/ipaddress> <server portnumber> /<filename.extension> <extendedproxy ipaddress> <extendedproxy portnumber> <time_in_seconds>
```
Note: Here, Time in seconds refers to actual seconds for the proxy cache timeout suppose 60 for 60 seconds.

## Authors

- Kritik Agarwal (CS23MTECH11009)
- Malsawmsanga Sailo (CS23MTECH11010)
- Bendi Satya Sai Sateesh (SM23MTECH11001)
