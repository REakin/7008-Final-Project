# import yaml
import socket
import random

def main():
    #create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.bind((cfg["EMULATOR"]["IP"], cfg["EMULATOR"]["T_PORT"]))
    s.bind(("127.0.0.1", 6005))

    dropPrecentage = 10

    while True:
        dropChance=random.randint(0,100)
        #send packet based off address
        packet = s.recv(2000)
        data = packet.decode()
        _switch = data[0]#1
        _flag = data[1:3]#2
        _seqnum = data[3:19]#16
        _windowsize = data[19:31]#12
        _data = data[31:]#payload

        if dropChance < dropPrecentage:
            print("Packet dropped"+str(dropChance))
        elif _switch == "1":
            s.sendto(packet, ("127.0.0.1", 7005))
        elif _switch == "0":
            s.sendto(packet, ("127.0.0.1", 5005))

if __name__ == '__main__':
    # with open('config.yml', 'r') as ymlfile:
    #     cfg = yaml.load(ymlfile)
    main()