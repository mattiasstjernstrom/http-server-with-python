import socket


def handle_request(request):
    """Handles the HTTP request."""
    filename = request.split()[1]
    if filename == "/":
        filename = "/index.html"

    try:
        with open("htdocs" + filename) as fin:
            content = fin.read()
        return "HTTP/1.0 200 OK\n\n" + content
    except FileNotFoundError:
        return "HTTP/1.0 404 NOT FOUND\n\nFile Not Found"


# Define socket host and port
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8080

# Create and configure socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    print(f"Listening on port {SERVER_PORT} ...")

    while True:
        client_connection, client_address = server_socket.accept()
        with client_connection:
            request = client_connection.recv(1024).decode()
            print(request)
            response = handle_request(request)
            client_connection.sendall(response.encode())
