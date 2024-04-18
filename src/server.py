import socket
import threading

IP = "localhost"
PORT = 5500
DELIM = b'\0'
MAX = 1024

clients = []
nicks = []

def recv_msg(socket):
    msg = ""
    data = b''
    while not msg:
        recv = socket.recv(MAX)
        if not recv:
            raise ConnectionError("Connection error!")
        data += recv
        if DELIM in recv:
            msg = data.rstrip(DELIM)
    return msg.decode()

def prep_msg(msg):
    msg += DELIM.decode()
    return msg.encode()

def send_msg(msg, socket):
    msg = prep_msg(msg)
    socket.sendall(msg)

def broadcast(msg):
    msg = prep_msg(msg)
    for c in clients:
        c.sendall(msg)

def handle_client(client):
    index = clients.index(client)
    nickname = nicks[index]
    while True:
        try:
            msg = recv_msg(client)
            if msg == "q":
                client.close()
                clients.remove(client)
                nicks.remove(nickname)
                print("Connection closed")
                break
            message = nickname + " : " + msg
            broadcast(message)
        except socket.error:
            client.close()
            clients.remove(client)
            nicks.remove(nickname)
            print("Connection closed")
            break

if __name__ == "__main__":
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((IP, PORT))
        server.listen()
        print(f"Server is listneng on: ", server.getsockname())
        while True:
            client, address = server.accept()
            send_msg("Choose your nick:", client)
            nick = recv_msg(client)
            clients.append(client)
            nicks.append(nick)
            threading.Thread(target=handle_client, args=(client, )).start()
            print("New connection started")
    except socket.error:
        print("Socket error!")
        