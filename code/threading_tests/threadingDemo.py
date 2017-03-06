import threading
from time import sleep

def worker(num):
    """thread worker function"""
    print 'Worker: %s' % num
    return



def main():
    threads = []
    print 'Spawning...'
    for i in range(5):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()
    print 'Joining...'
    for i in range(len(threads)):
        threads[i].join()
    print 'Exiting...'

if __name__ == '__main__':
    main()
