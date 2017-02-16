import sys
import serial #see github for download/installation via: 'python setup.py install'

ser = serial.Serial()
ser.port = 'COM4' #try this first
ser.baud = 9600
for num in range(1,100): #assuming USB-serial only windows PC connection
    try:
        ser.close()
        ser.open()
        break
    except:
        ser.port = 'COM' + str(num) #ex: 'COM20'
        ser.baudrate = 9600
print 'Opened Serial Port: ' + str(ser.name)

connected = False
while not connected:
    serin = ser.read()
    connected = True

try:
    while(1):
        data = ser.readline() #wait(infinite) for '\n', then return str()
        sep  = data.split()   #create list() seperated by whitespace ('\t')
        line = ''
        line = ','.join(sep) + '\n'
        print line
        with open('data.csv', 'a') as file:
            file.write(line)
except:
    pass
ser.close() # close serial port
 