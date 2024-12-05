import socket
import threading


# Setting up the server
def server_setup(host='127.0.0.1', port=49999):
    s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_sock.bind((host, port))
    s_sock.listen()
    print("Server started listening to connections")
    
    while True:
        client_socket, client_address = s_sock.accept()
        print("Server accepted the connection..!")
        
if __name__ == "__main__":
    server_setup()
