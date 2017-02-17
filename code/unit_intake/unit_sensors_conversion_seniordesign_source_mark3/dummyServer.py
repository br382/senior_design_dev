import socket
import threading

def launchDummyServer():
    threading.Thread(target=server, args=(3.0,)).start() #simple thread without handling methods
    #functually equivaliant to: thread.start_new_thread(server,(3.0))

def server(timeout=1.0): #timeout is in seconds
    import socket
    H              = 'localhost' #done here on purpose...
    P              = 12345
    SERVERRESPONSE = 'hello client, said the server.'
    sock           = socket.socket()
    sock.bind((H, P))
    print ['(SOCKETHOST, SOCKETPORT)', (H, P)]
    sock.listen(5)
    while True:
        socket_connection, addr = sock.accept()
        socket_connection.settimeout(timeout)
        client_msg_str        = socket_connection.recv(1024)
        if client_msg_str:
            print 'From: ' + str(addr) + ', Data: ' + str([client_msg_str])
            socket_connection.send(SERVERRESPONSE)
            print 'From: ' + 'Server (me)' + ', ' + 'Data: ' + str([SERVERRESPONSE])
            socket_connection.close()
            print 'Closed: ' + 'Client on ' + str(addr)
            break
        socket_connection.close()
        print 'Closed: ' + 'Client on ' + str(addr)
    print '========= Closing Thread of launchDummyServer() =========='

if __name__ == '__main__':
    try:
        while(1):
            server()
    except:
        pass