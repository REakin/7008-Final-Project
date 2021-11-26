import json
import socket

def main():
    writing = ""
    #create main loop
    while True:
        #create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #create connection
        #s.bind((cfg["RECEIVER"][0]["IP"], cfg["RECEIVER"][0]["PORT"]))
        s.bind(('127.0.0.1', 7005))
        #open file
        f = None
        while True:
            #recive packet
            data = s.recv(2000).decode()
            #if packet is not empty
            if data:
                #write packet to file
                #syn/ack|flags|window size|seqnum|data
                _switch = data[0]#1
                _flag = data[1:3]#2
                _seqnum = data[3:19]#16
                _windowsize = data[20:32]#12
                _data = data[33:]#payload
                if _switch == '1': # SYN packet
                    print("SYN packet received")
                    if _flag == '11': #flag for EOF
                        print("EOF flag")
                        f = open("output.txt", "w")
                        f.write(writing)
                        f.close()
                        break
                    if _flag == '10': #flag for filename
                        print("Filename flag")
                        f = open(_data, "w")
                    if _flag == '01': #flag for data
                        print("Data flag")
                        #convert seqnum from binary to decimal
                        offset = int(_seqnum, 2)
                        print(offset)
                        writing = writing[:offset]+_data
                    # send ACK=0 back
                    s.sendto(b'0' + b'00' + _seqnum.encode() + _windowsize.encode(), ('127.0.0.1', 5005))

if (__name__ == '__main__'):
    with open("config.json", "r") as read_file:
        cfg = json.load(read_file)
    main()