#!/usr/bin/env python3
import socket
import json
import time

def main():
    #create main loop
    while True:
        #create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # s.bind((cfg["TRANSMITTER"]["IP"], cfg["TRANSMITTER"]["PORT"]))
        s.bind(("127.0.0.1", 5005))
        f = open("Blanchette.txt", 'rb')
        data = f.read()
        windowsize = 2
        seqnum = 0 #the offset number
        #close file
        f.close()

        #start three way handshake
        #send SYN
        print("starting three way handshake")
        s.sendto(b"1000000000000000000000000000", ("127.0.0.1", 7005))
        #recieve ACK
        s.settimeout(3)
        try:
            _data, addr = s.recvfrom(1024)
            if _data:
                print("ACK received")
        except socket.timeout:
            print("timeout")
            exit(0)
    
        # packet = s.recvfrom(1059)
        # message = packet[0].decode()
        # address = packet[1]

        while True:
            time.sleep(0.5)
            #send packet
            #increase window size by two times the current each time until a maximum of 1024
            _seqnum = '{0:016b}'.format(int(seqnum))
            _windowsize = '{0:012b}'.format(int(windowsize))

            if(seqnum > len(data)):
                packetdata = "1"+"11"+_seqnum+_windowsize
                packetdata = packetdata.encode()
                packetdata += data[int(seqnum):int(seqnum+windowsize)]
            else:
                packetdata = "1"+"01"+_seqnum+_windowsize
                packetdata = packetdata.encode()
                packetdata += data[int(seqnum):int(seqnum+windowsize)]
            # print(packetdata)
            s.sendto(packetdata,("127.0.0.1",7005))
            #set a timeout for the packet if a ack is not recieved
            s.settimeout(3)
            try:
                #recieve packet
                ack = s.recv(1024).decode()
                # print(ack)
                _switch = ack[0]#1
                _flag = ack[1:3]#2
                _seqnum = ack[3:19]#16
                _windowsize = ack[20:32]#12
                _data = ack[33:]#payload

                #if the ack is correct, continue                
                if _switch == '0' and _seqnum == '{0:016b}'.format(int(seqnum)):
                    print("ACK recieved")
                    seqnum = seqnum + windowsize
                    if windowsize < 1024:
                        windowsize = windowsize * 2
                    continue
                if _switch == '0' and _flag == "11":
                    print("EOF ACK'ed")
                    print("closing connection")
                    s.close()
                    exit(0)
                #if the ack is incorrect, resend the packet
                else:
                    print("Incorrect ACK recived resending")
                    continue
            except socket.timeout:
                #if the packet times out, resend the packet
                print("timeout (reducing windowsize)")
                windowsize = windowsize / 2
                if(windowsize < 1):
                    windowsize = 1
                continue
            #if the packet is sent, continue

if __name__ == '__main__':
    # with open('config.yaml', 'r') as ymlfile:
    #     cfg = yaml.load(ymlfile)
    main()