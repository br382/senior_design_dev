#!/usr/bin/python

import thread
import time

# Define a function for the thread
def print_time( threadName, delay):
   count = 0
   while count < 5:
      time.sleep(delay)
      count += 1
      print "%s: %s" % ( threadName, time.ctime(time.time()) )

def main():
    print 'Spawning...'
    try:
        thread.start_new_thread( print_time, ("Thread-1", 1, ) )
        thread.start_new_thread( print_time, ("Thread-2", 2, ) )
        print 'Working...'
    except:
        print "Error: Unable to start thread..."
    time.sleep(20)
    print 'Exiting...'
if __name__ == '__main__':
    main()