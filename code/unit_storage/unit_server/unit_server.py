"""
@Author Brett
"""
import socket
#import thread
from threading import Lock, Thread
from Database  import *
from Storage   import timestamp
from time      import sleep
try: #for debugging use only:
    from dummyUsers import *
except:
    pass

LOAD_LAST_DUMP    = False #Load old users data
SOCKETHOST        = externLocalIP() #'192.168.1.126' or 'localhost', etc...
SOCKETPORT        = 12345

def main(DEBUG=True):
    data = Database()
    if LOAD_LAST_DUMP:
        t = data.load() #load any previous instance, with timestamp 't'
        print 'Loaded Previous Data From: ' + str(t)
    if DEBUG:
        #for id in range(200,200): #add dummy users
        #    data.addUser(id)
        try:
            data.users = dummyUsers(users=3)
            print 'loading dummyUsers() Data'
            last  = timestamp()
        except:
            pass
    #if DEBUG: print ''
    #if DEBUG: s = data.serverWork('{"list_users":1}')
    #if DEBUG: print ''
    #if DEBUG: print 'list_users', s
    #if DEBUG: print ''
    data.lock = Lock() #add Lock() to database object
    sock      = socket.socket()
    while(1):
        try:
            sock.bind((SOCKETHOST, SOCKETPORT))
            break
        except:
            print 'Trying To Bind Socket', (SOCKETHOST, SOCKETPORT)
            sleep(1)
            pass
    print ['(SOCKETHOST, SOCKETPORT)', (SOCKETHOST, SOCKETPORT)]
    sock.listen(5)
    while True:
        print ''
        if DEBUG:
            try:
                if (timestamp() - last) > 2:
                    temp = dummyUsers(users=3)
                    for k in temp.keys():
                        data.users[k] = temp[k]
                    print 'loading dummyUsers() Data'
                    last = timestamp()
            except:
                pass
        client_instance, addr = sock.accept()
        #thread.start_new_thread(handler, (data, client_instance, addr, 1024, DEBUG))
        while(1):
            try:
                Thread(target=handler, args=(data, client_instance, addr, 1024, DEBUG)).start()
                break
            except:
                print 'Trying to Launch Thread'
                sleep(0.01)
                pass

def handler(database, socket_connection, addr, BUFF_SIZE=1024, DEBUG=False):
    if DEBUG: print timestamp(), 'Opening socket...'
    client_msg_str = socket_connection.recv(BUFF_SIZE)
    if DEBUG: print timestamp(), 'Socket opened'
    if client_msg_str:
        if DEBUG: print 'From: ' + str(addr) + ', Data: ' + str([client_msg_str])
        #
        if DEBUG: print timestamp(), 'Acquiring lock...'
        database.lock.acquire()
        if DEBUG: print timestamp(), 'Lock acquired'
        if DEBUG: logIP(addr)
        output_json_str = database.serverWork(client_msg_str)
        database.dump()
        if DEBUG: print timestamp(), 'Releasing lock...'
        database.lock.release()
        if DEBUG: print timestamp(), 'Lock released'
        #
        socket_connection.send(output_json_str)
        if DEBUG: print 'From: ' + 'Server (me)' + ', ' + 'Data: ' + str([output_json_str])
    if DEBUG: print timestamp(), 'Closing socket...'
    socket_connection.close()
    if DEBUG: print timestamp(), 'Socket closed'
    if DEBUG: print 'Closed: ' + 'Client on ' + str(addr)
    return None

def logIP(client_ip, filename='ip.log'):
    with open(filename, 'a') as file:
        line = ''
        try:
            line += str(client_ip)
            line += ' '
            line += str(timestamp())
            line += '\n'
        except:
            print 'ERROR logIP(): ' + line
        file.write(line)

if __name__ == '__main__':
    main()
