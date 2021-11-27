import json
import socket

def main():
    writing = ""
    filename = ""
    f = None
    #create main loop
    while True:
        #create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #create connection
        #s.bind((cfg["RECEIVER"][0]["IP"], cfg["RECEIVER"][0]["PORT"]))
        s.bind(('127.0.0.1', 7005))
        #open file
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
                _windowsize = data[19:31]#12
                _data = data[31:]#payload
                if _switch == '1': # SYN packet
                    print("SYN packet received")
                    if _flag == '11': #flag for EOF
                        print("EOF flag")
                        f = open(filename, "w")
                        f.write(writing)
                        f.close()
                        #set flag to ACK EOF
                        _flag = '11'
                    elif _flag == '10': #flag for filename
                        print("Filename flag")
                        open(_data, "w")
                        filename = _data
                    elif _flag == '01': #flag for data
                        print("Data flag")
                        #convert seqnum from binary to decimal
                        offset = int(_seqnum, 2)
                        print(_data)
                        writing = writing[:offset+1]+_data
                        _flag = '00'
                    # send ACK=0 back
                    s.sendto(b'0' + _flag.encode() + _seqnum.encode() + _windowsize.encode(), ('127.0.0.1', 6005))

if (__name__ == '__main__'):
    with open("config.json", "r") as read_file:
        cfg = json.load(read_file)
    main()