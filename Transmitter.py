import yaml
import socket

def main():
    #create main loop
    while True:
        #create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((cfg["TRANSMITTER"]["IP"], cfg["TRANSMITTER"]["PORT"]))
        f = open(cfg["TargetFile"], 'r')

        data = f.read()
        windowsize = 2
        seqnum = 0 #the offset number
        #close file
        f.close()
        #create connection
        conn, addr = s.accept()
        print('Connected by', addr)
        while True:
            #send packet
            #increase window size by two times the current each time until a maximum of 1028
            if windowsize < 1024:
                windowsize = windowsize * 2
            packetdata = data[seqnum:seqnum+windowsize]
            seqnum = seqnum + windowsize

            conn.send(packetdata.encode())
            #set a timeout for the packet if a ack is not recieved
            conn.settimeout(1)
            try:
                #recieve packet
                ack = conn.recv(1024)
                #if the ack is correct, continue
                if ack == b'ACK':
                    continue
                #if the ack is incorrect, resend the packet
                else:
                    conn.send(packetdata.encode())
            except socket.timeout:
                #if the packet times out, resend the packet
                conn.send(packetdata.encode())
            #if the packet is sent, continue
            continue
            break

if __name__ == '__main__':
    with open('config.yml', 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    main()