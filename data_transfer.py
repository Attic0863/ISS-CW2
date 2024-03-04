import socket
import ssl

# ssl encryption will be used to transfer data and will also utilise the key_management class which will generate RSA
# private public keys which will be used in data transfer as well to further secure data.
class DataTransfer:
    # ssl context gets made
    def create_ssl_context(self, ca_cert=None, certfile=None, keyfile=None):
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=ca_cert)
        if certfile and keyfile:
            context.load_cert_chain(certfile=certfile, keyfile=keyfile)
        return context

    # initiates connection with ssl context
    def connect_secure(self, address, port, ssl_context):
        sock = socket.create_connection((address, port))
        return ssl_context.wrap_socket(sock, server_hostname=address)

    # sending data function
    def send_data_secure(self, ssl_socket, data):
        ssl_socket.sendall(data.encode())

    # receiving data function
    def receive_data_secure(self, ssl_socket, buffer_size=4096):
        received_data = b""
        while True:
            chunk = ssl_socket.recv(buffer_size)
            if not chunk:
                break
            received_data += chunk
        return received_data.decode()
