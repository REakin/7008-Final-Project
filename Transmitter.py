#!/usr/bin/env python3
import socket
import json

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
        s.sendto(b"SYN", ("127.0.0.1", 5006))
        #recieve ACK
        packet = s.recvfrom(1059)
        message = packet[0].decode()
        address = packet[1]

        while True:
            #send packet
            #increase window size by two times the current each time until a maximum of 1024
            _seqnum = '{0:016b}'.format(seqnum)
            _windowsize = '{0:012b}'.format(windowsize)

            packetdata = "0"+"01"+_seqnum+_windowsize
            packetdata = packetdata.encode()
            packetdata += data[seqnum:seqnum+windowsize]
            s.sendto(packetdata,("127.0.0.1",5006))
            #set a timeout for the packet if a ack is not recieved
            s.settimeout(3)
            try:
                #recieve packet
                ack = s.recvfrom(1024)
                #if the ack is correct, continue
                if ack == b'ACK' + str(seqnum).encode():
                    print("ACK recieved")
                    seqnum = seqnum + windowsize
                    if windowsize < 1024:
                        windowsize = windowsize * 2
                    continue
                #if the ack is incorrect, resend the packet
                else:
                    continue
            except socket.timeout:
                #if the packet times out, resend the packet
                print("timeout")
                windowsize = windowsize / 2
                if(windowsize < 1):
                    windowsize = 1
                continue
            #if the packet is sent, continue

if __name__ == '__main__':
    # with open('config.yaml', 'r') as ymlfile:
    #     cfg = yaml.load(ymlfile)
    main()