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
        #open file
        f = open('blanchette.txt', 'r')
        #read file
        data = f.read()
        #close file
        f.close()
        #parse data into 60 byte chunks
        data = [data[i:i+60] for i in range(0, len(data), 60)]
        #create connection
        conn, addr = s.accept()
        print('Connected by', addr)
        while True:
            #send data
            for i in data:
                conn.send(i.encode())
            #close connection
            conn.close()
            break

if __name__ == '__main__':
    main()