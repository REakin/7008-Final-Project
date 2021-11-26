# import yaml
import socket

def main():
    #create main loop
    while True:
        #create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #create connection
        # s.bind((cfg["EMULATOR"]["IP"], cfg["EMULATOR"]["T_PORT"]))
        s.bind(("127.0.0.1", 5006))
        # s2.bind((cfg["EMULATOR"]["IP"], cfg["EMULATOR"]["R_PORT"]))
        #create thread
        while True:
            #send packet based off address
            packet = s.recvfrom(1024)
            address = packet[1]

            data = packet[0].decode()
            _switch = data[0]#1
            _flag = data[1:2]#2
            _window = data[3:6]#4
            _seqnum = data[7:22]#16
            _windowsize = data[23:34]#12
            _data = data[35:]#payload

            if address[0] == "127.0.0.1":
                if not _data:
                    break
                s.sendto(b"ACK"+b"0",("127.0.0.1",5005))

                
            #recieve packet based off address
            # elif addr[0] == cfg["TRANSMITTER"]["IP"]:
            #     data = conn.recv(1024)
            #     if not data:
            #         break
            #     print(data)
            #     conn.send(data)
        s.close()

if __name__ == '__main__':
    # with open('config.yml', 'r') as ymlfile:
    #     cfg = yaml.load(ymlfile)
    main()