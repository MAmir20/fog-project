import socket

# Setup server for aggregation
def start_server():
    host = 'localhost'
    port = 5000  # You can change this to any port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server started at {host}:{port}")
        
        while True:
            client_socket, addr = server_socket.accept()
            with client_socket:
                print(f"Connected by {addr}")
                data = client_socket.recv(1024)
                if data:
                    print(f"Data received: {data.decode()}")

if __name__ == "__main__":
    start_server()
