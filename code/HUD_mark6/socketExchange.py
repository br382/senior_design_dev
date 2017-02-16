#!/usr/bin/python
"""
@Author Brett
    main() #self-test of all methods
    externLocalIP() return '192.168.1.782' or similar dynamically assigned number (hopefully not localhost)
    socketExchange(msg, SOCKET, buf=1024, timeout=1.0, DEBUG=False) #send msg to SOCKET, return '' else None
    pick(d) #for d<=dict(): {{return (dict().keys() not None), also del[k] if k == None}, else if len(.keys() not None) == 0 return None}
    socketExchangeDict(msg, server_dict, buf=1024, timeout=1.0, DEBUG=False) #try all SOCKET's in server_dict, return '' or None on all failure.
    scanServers(ip_start='127.0.0.1', port=12345,r=3, DEBUG=False) #generate socket_dict for socketExchangeDict()
"""
import socket               # Import socket module
import threading
from time import sleep

def main():
    print '========= Testing socketExchange =========='
    #Test socketExchange() method:
    print '========= Spawning launchDummyServer() =========='
    launchDummyServer()
    #
    SOCKETHOST = 'localhost' #done here on purpose...
    SOCKETPORT = 12345
    SOCKET     = (SOCKETHOST, SOCKETPORT)
    snd_msg    = 'from function to server'
    print snd_msg
    print '========= Calling socketExchange() =========='
    rec_msg    = socketExchange(snd_msg, SOCKET, timeout=2.0, DEBUG=True)
    print rec_msg
    sleep(3)
    print '========= Testing scanServers() =========='
    #Now Test Server Scanning:
    scanServers(DEBUG=True)
    print '========= Exiting... =========='
    sleep(3)

def externLocalIP():
    return socket.gethostbyname('localhost')
    try:
        return ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
    except:
        #failure to attach to networking device
        return socket.gethostbyname('localhost')

def socketExchange(msg, SOCKET, buf=1024, timeout=1.0, DEBUG=False): #timeout is in seconds
    try:
        SOCKETHOST, SOCKETPORT = SOCKET
        if DEBUG: print 'Sending Data To: ', SOCKET
        sock     = socket.socket(socket.AF_INET)
        sock.connect((SOCKETHOST, SOCKETPORT))
        sock.settimeout(timeout)
        val      = sock.send(msg)
        if DEBUG: print 'From: ' + 'Client (me)' + ', Data: ' + str([msg])
        ret      = sock.recv(buf)
        if DEBUG: print 'From: ' + str((SOCKETHOST, SOCKETPORT)) + ', Data: ' + str([ret])
        sock.close()
        if DEBUG: print 'Closed: Server on ' + str((SOCKETHOST, SOCKETPORT))
    except:
        if DEBUG: print 'Data Failed...'
        return None
    return ret

def pick(d):
    for k in d:
        if d[k] == None:
            del d[k]
        else:
            return k
    return None

def socketExchangeDict(msg, server_dict, buf=1024, timeout=1.0, DEBUG=False):
    i = 0
    while(len(server_dict)>0):
        i += 1
        if DEBUG: print 'itter ', i
        s = pick(server_dict)
        ret = socketExchange(msg, s, buf=buf, timeout=timeout, DEBUG=DEBUG)
        if DEBUG: print 'SOCKETEXCHANGEDICT ret: ', ret
        if ret == None:
            del server_dict[s]
        else:
            return ret
    return None

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

def _scan(procnum, socket, ret_dict, lock, DEBUG=False):
    msg = '{"ping":1}'
    if DEBUG: 'to ', socket
    ret = socketExchange(msg, socket)
    if DEBUG: '  ', socket, ' sent ', ret
    lock.acquire()
    ret_dict[socket] = ret
    lock.release()

def scanServers(ip_start=externLocalIP(), port=12345,r=3, ret_dict={}, DEBUG=False):
    #'r' specifies which range of the ip to scan, r=3 is only the 4th (last in IPv4), 1 or 0 is all ranges
    ip            = ip_start
    lock = threading.Lock()
    ip_r  = ip.split('.')
    check = ''
    th    = []
    m     = 256
    ip_n  = []
    uid   = 0
    if DEBUG: print 'My Local Network IP is: ' + str(ip)
    if DEBUG: print 'Creating Work Pool...'
    for d in ip_r:
        ip_n.append(int(d))
    for i in range(len(ip_n)):
        for j in range(m):
            if i >= r:
                ip_n[i] = j
                check = '.'.join(str(p) for p in ip_n)
                s = (check,port)
                th.append(threading.Thread(target=_scan, args=(uid, s, ret_dict, lock)))
                uid += 1
    if DEBUG: print 'Spawning Threads...'
    for t in th:
        t.start()
    if DEBUG: print 'Waiting for all ' + str(len(th)) + ' Threads to finish.'
    for t in th:
        t.join()
    if DEBUG: print 'Done Scanning... ' + str(len(ret_dict)) + ' Items Returned.'
    for k in ret_dict.keys():
        if ret_dict[k] == None:
            del ret_dict[k]
    if DEBUG: print ret_dict
    return dict(ret_dict) #format: {(ip_0, port_0): 'server_response', (ip_1, port_1): None}

if __name__ == '__main__':
    main()
    
