import socket
import os
import mimetypes
from template import Template


def tcp_server():
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 8080
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen()
    print('Listen on http://127.0.0.1:8080')

    while True:
        client_connection, client_address = server_socket.accept()
        request = client_connection.recv(1024).decode()
        print('Request:', request)
        # handle request
        if request and request.strip():
            response = handle_request(request)
            client_connection.sendall(response)
        client_connection.close()

    server_socket.close()


def handle_request(request):
    request_message = request.split("\r\n")
    request_line = request_message[0]
    words = request_line.split()
    method = words[0]
    uri = words[1].strip("/")

    http_version = words[2]
    if uri == '':
        _POST = {}
        username = _POST.get('username')
        password = _POST.get('password')
        if username == 'user' and password == 'user':
            # Redirect to home page after successful login
            response_line = f'{http_version} 302 Found'
            entity_header = 'Location: home'
            response = generate_response(response_line, entity_header, b'')
    elif uri == 'home':
        uri = 'index.html'

    if method == 'GET':
        response = handle_get(uri, http_version)
    elif method == 'POST':
        data = request_message[-1]
        response = handle_post(uri, http_version, data)
    else:
        response = generate_response(http_version, '400 Bad Request', '')

    return response


def handle_get(uri, http_version):
    file_path = f'htdocs/{uri}'
    if os.path.exists(file_path) and not os.path.isdir(file_path):
        response_line = f'{http_version} 200 OK'
        content_type = mimetypes.guess_type(file_path)[0] or 'text/html'
        entity_header = f'Content-Type: {content_type}'
        with open(file_path, 'rb') as file:
            message_body = file.read()
        response = generate_response(response_line, entity_header, message_body)
    else:
        response_line = f'{http_version} 404 Not Found'
        entity_header = 'Content-Type: text/html'
        message_body = b'<h1>404 Not Found</h1>'
        response = generate_response(response_line, entity_header, message_body)
    if uri == '':
        uri = 'login.html'

    if uri == 'home':
        response_line = f'{http_version} 302 Found'
        entity_header = 'Location: login.html'
        message_body = b''
        response = generate_response(response_line, entity_header, message_body)
        return response

    file_path = f'htdocs/{uri}'
    if os.path.exists(file_path) and not os.path.isdir(file_path):
        response_line = f'{http_version} 200 OK'
        content_type = mimetypes.guess_type(file_path)[0] or 'text/html'
        entity_header = f'Content-Type: {content_type}'
        with open(file_path, 'rb') as file:
            message_body = file.read()
        response = generate_response(response_line, entity_header, message_body)
    else:
        response_line = f'{http_version} 404 Not Found'
        entity_header = 'Content-Type: text/html'
        message_body = b'<h1>404 Not Found</h1>'
        response = generate_response(response_line, entity_header, message_body)

    return response


def handle_post(uri, http_version, data):
    file_path = f'htdocs/{uri}'
    if os.path.exists(file_path) and not os.path.isdir(file_path):
        response_line = f'{http_version} 200 OK'
        content_type = mimetypes.guess_type(file_path)[0] or 'text/html'
        entity_header = f'Content-Type: {content_type}'

        with open(file_path, 'r') as file:
            html = file.read()

        _POST = {}
        for i in data.split("&"):
            x = i.split("=")
            _POST[x[0]] = x[1]
        context = {'_POST': _POST}
        t = Template(html)
        message_body = t.render(context).encode()
        response = generate_response(response_line, entity_header, message_body)
    else:
        response_line = f'{http_version} 404 Not Found'
        entity_header = 'Content-Type: text/html'
        message_body = b'<h1>404 Not Found</h1>'
        response = generate_response(response_line, entity_header, message_body)

    return response


def generate_response(response_line, entity_header, message_body):
    crlf = '\r\n'
    response = f'{response_line}{crlf}{entity_header}{crlf}{crlf}'.encode() + message_body
    return response


if __name__ == "__main__":
    tcp_server()
