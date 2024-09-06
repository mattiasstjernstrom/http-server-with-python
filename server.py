import socket
from threading import Thread


def get_local_ip():
    """Gets the local IP address of the machine."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]


def handle_request(client_connection):
    """Handles the HTTP request."""
    request = client_connection.recv(1024).decode()
    print(request)

    filename = request.split()[1]
    if filename == "/":
        filename = "/index.html"

    try:
        with open("htdocs" + filename) as fin:
            content = fin.read()
        response = "HTTP/1.0 200 OK\n\n" + content
    except FileNotFoundError:
        response = "HTTP/1.0 404 NOT FOUND\n\nFile Not Found"

    client_connection.sendall(response.encode())
    client_connection.close()


def start_server(host, port):
    """Starts the server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"{host}:{port}, ")

        while True:
            client_connection, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")
            handle_request(client_connection)


if __name__ == "__main__":
    local_ip = get_local_ip()
    SERVER_PORT = 8080

    print(f"Starting server at: ")

    Thread(target=start_server, args=("127.0.0.1", SERVER_PORT)).start()
    Thread(target=start_server, args=(local_ip, SERVER_PORT)).start()
    print()
