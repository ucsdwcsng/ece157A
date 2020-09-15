import sys
import os

# run the command to generate usb.dat
cmd1 = 'iio_info -s | grep "usb" | awk \'{print $9}\' | awk -F[ \'{print $2}\' | awk -F] \'{print $1}\' > usb.dat'
os.system(cmd1)

# open usb.dat and print its entries
f = open('usb.dat','r')

strUSB = f.readlines()                  # read all the lines from iio_info -s
num_devices = len(strUSB)-1             # get the number of devices

# clean-up
f.close()                               # close file once we're done.

# remove file
cmd2 = 'rm usb.dat'
os.system(cmd2)


if num_devices > 0:
    strUSB = strUSB[1:]

    for n in range(num_devices):
        strUSB[n] = strUSB[n].rstrip()  # strip the "\n" chars out

    TX = strUSB[0]
    RX = strUSB[1]

    print('TX set to Pluto: ' + TX)
    print('Rx set to Pluto: ' + RX)
else:
    print('No Devices Found!')

print('\n')

#print(strUSB)                           # debug print          
