try:
    import uuid
except:
    import time
    def timestamp():
        return time.time()

def main():
    for i in xrange(3):
        print uidGen()
    
def uidGen():
    try:
        return str(uuid.uuid4())
    except:
        return str(timestamp())
    
if __name__ == '__main__':
    main()