import yaml
import socket

def main():
    #create main loop
    while True:
        #create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #create connection
        s.bind((cfg["RECEIVER"]["IP"], cfg["RECEIVER"]["PORT"]))
        #open file
        f = open("received_file.txt", "wb")
        #create connection
        conn, addr = s.accept()
        print('Connected by', addr)
        while True:
            #recive packet
            data = conn.recv(1024)
            for i in data:
                #write data to file
                f.write(i)
            #close connection
            conn.close()
            break
        #close file
        f.close()

if __name__ == '__main__':
    with open('config.yml', 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    main()