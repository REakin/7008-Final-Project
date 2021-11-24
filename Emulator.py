import yaml
import socket

def main():
    #create main loop
    while True:
        #create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #create connection
        s.bind((cfg["EMULATOR"]["IP"], cfg["EMULATOR"]["T_PORT"]))
        s2.bind((cfg["EMULATOR"]["IP"], cfg["EMULATOR"]["R_PORT"]))
        #create thread
        s.listen(1)
        #create recieve and send
        conn, addr = s.accept()
        print('Connected by', addr)
        while True:
            #send packet based off address
            if addr[0] == cfg["RECEIVER"]["IP"]:
                data = conn.recv(1024)
                if not data:
                    break
                print(data)
                conn.send(data)
            #recieve packet based off address
            elif addr[0] == cfg["TRANSMITTER"]["IP"]:
                data = conn.recv(1024)
                if not data:
                    break
                print(data)
                conn.send(data)
        conn.close()

if __name__ == '__main__':
    with open('config.yml', 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    main()