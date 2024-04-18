import socket
import threading

IP = "localhost"
PORT = 5500
DELIM = b'\0'
MAX = 1024

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

def send(socket):
    while True:
        try:
            msg = input()
            if msg == "":
                continue
            send_msg(msg, socket)
            if msg == "q":
                send_msg(msg, client)
                client.close()
                break
        except socket.error:
            print("Error when sending message")
            socket.close()
            break

def recieve(socket):
    while True:
        try:
            msg = recv_msg(socket)
            print(msg)
        except socket.error:
            print("error when receiving message!")
            client.close()
            break

if __name__ == "__main__":
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((IP, PORT))
        reply = recv_msg(client)
        print(reply)
        nick = input()
        send_msg(nick, client)
        print("Press q to close the connection")
        send_thread = threading.Thread(target=send, args=(client, )).start()
        recv_thread = threading.Thread(target=recieve, args=(client, )).start()
    except socket.error:
        print("Client error!")
        