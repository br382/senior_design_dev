#!/usr/bin/python
"""
@Author Brett
Sends string to server, and waits for reply back.
If valid, returns sock.recv(buf), else returns None.
"""
import socket               # Import socket module
#import sys

def main():
    launchDummyServer()
    #
    SOCKETHOST = 'localhost'
    SOCKETPORT = 12345
    SOCKET     = (SOCKETHOST, SOCKETPORT)
    snd_msg    = 'from function to server'
    print snd_msg
    rec_msg    = socketEchange(snd_msg, SOCKET, DEBUG=True)
    print rec_msg

def socketExchange(msg, SOCKET, buf=1024, DEBUG=False):
    #print 'Inside socketExchange()'
    try:
        SOCKETHOST, SOCKETPORT = SOCKET
        #print 'Sending Data To: ', SOCKET
        sock     = socket.socket(socket.AF_INET)
        sock.connect((SOCKETHOST, SOCKETPORT))
        val      = sock.send(msg)
        if DEBUG: print 'From: ' + 'Client (me)' + ', Data: ' + str([msg])
        ret      = sock.recv(buf)
        if DEBUG: print 'From: ' + str((SOCKETHOST, SOCKETPORT)) + ', Data: ' + str([ret])
        sock.close()
        if DEBUG: print 'Closed: Server on ' + str((SOCKETHOST, SOCKETPORT))
    except:
        print 'Data Failed...'
        return None
    return ret

def launchDummyServer():
    import thread
    thread.start_new_thread(server, ())

def server():
    import socket
    H              = 'localhost'
    P              = 12345
    SERVERRESPONSE = 'hello client, said the server.'
    sock           = socket.socket()
    sock.bind((H, P))
    print ['(SOCKETHOST, SOCKETPORT)', (H, P)]
    sock.listen(5)
    while True:
        socket_connection, addr = sock.accept()
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
        

if __name__ == '__main__':
    main()
