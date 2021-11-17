#create main loop
#create socket
#create connection
#create thread
#create recieve and send
CLIENT_IP="192.168.1.0"
SERVER_IP="192.168.1.1"

def main():
    #create main loop
    while True:
        #create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #create connection
        s.bind(('', 8080))
        #create thread
        s.listen(1)
        #create recieve and send
        conn, addr = s.accept()
        print('Connected by', addr)
        while True:
            #send packet based off address
            if addr[0] == CLIENT_IP:
                data = conn.recv(1024)
                if not data:
                    break
                print(data)
                conn.send(data)
            #recieve packet based off address
            elif addr[0] == SERVER_IP:
                data = conn.recv(1024)
                if not data:
                    break
                print(data)
                conn.send(data)
        conn.close()

if __name__ == '__main__':
    main()