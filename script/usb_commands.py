# coding=UTF-8
import usb
import time
import datetime
import os
import struct
import array
import math
import smath

dev = None

COMMAND_SET_LED = 1
COMMAND_SET_FREQUENCY = 2
COMMAND_ADC_START = 3
COMMAND_ADC_READ_BUFFER = 4
COMMAND_ADC_ELAPSED_TIME = 5
COMMAND_START_SYNCHRO = 6

PERIOD_ROUND120 = [
        #720000, #100.00 Hz
        #360000, #200.00 Hz
        #240000, #300.00 Hz
        #180000, #400.00 Hz
        #144000, #500.00 Hz
        120000, #600.00 Hz
        102840, #700.12 Hz
        90000, #800.00 Hz
        79920, #900.90 Hz
        72000, #1000.00 Hz
        36000, #2000.00 Hz
        24000, #3000.00 Hz
        18000, #4000.00 Hz
        14400, #5000.00 Hz
        12000, #6000.00 Hz
        10200, #7058.82 Hz
        9000, #8000.00 Hz
        7920, #9090.91 Hz
        7200, #10000.00 Hz
        3600, #20000.00 Hz
        2400, #30000.00 Hz
        1800, #40000.00 Hz
        1440, #50000.00 Hz
        1200, #60000.00 Hz
        960, #75000.00 Hz
        840, #85714.29 Hz
        720, #100000.00 Hz
        600, #120000.00 Hz
        480, #150000.00 Hz
        ]


def findDevice():
    global dev
    dev = usb.core.find(idVendor=0x16C0, idProduct=0x05DC)

    if dev is None:
    	raise ValueError('Device not found')
    else:
        print "Device found"

    dev.set_configuration()

def readAll():
    time.sleep(0.1)
    while True:
        try:
            data = dev.read(129, 128, interface=1, timeout=50)
            if len(data)==0:
                break
            print "readb=", data
            print "read=", data.tostring()
        except usb.core.USBError:
            break
    pass

def readOne():
    time.sleep(0.1)
    try:
        data = dev.read(129, 128, interface=1, timeout=50)
        if len(data)==0:
            print "Read empty"
        else:
            print "readb=", data
    except usb.core.USBError:
        print "Read USB error"
    pass

def readInt():
    data = dev.read(129, 128, interface=1, timeout=50)
    if len(data)!=4:
        print "Fail read int len="+str(len(data))
    else:
        print data[0]+data[1]*0x100+data[2]*0x10000+data[3]*0x1000000

def readCommand():
    time.sleep(0.01)
    try:
        data = dev.read(129, 128, interface=1, timeout=50)
        if len(data)==0:
            print "Read empty"
            return
        else:
            print "readb=", data
    except usb.core.USBError:
        print "Read USB error"
        return

    cmd = data[0]
    if cmd==COMMAND_SET_LED:
        print "Set led="+str(data[1]) 
    elif cmd==COMMAND_SET_FREQUENCY:
        period = struct.unpack_from('I', data, 1)[0]
        clock = struct.unpack_from('I', data, 5)[0]
        print "period=",period
        print "clock=",clock
        print "F=",clock/float(period)
    elif cmd==COMMAND_ADC_START:
        print "adcStart"
    elif cmd==COMMAND_ADC_ELAPSED_TIME:
        print "Elapset ticks=", struct.unpack_from('I', data, 1)[0]
    elif cmd==COMMAND_START_SYNCHRO:
        (period, clock, adc_cycles) = struct.unpack_from('=III', data, 1)
        print "period=",period
        print "clock=",clock
        print "F=",clock/float(period)
        print "adc_cycles=", adc_cycles
    else:
        print "Unknown command="+str(data[0])
    pass
"""
def readConversionData():
    with open("out.dat", "wb") as file:
        step = 30
        for i in xrange(0, 34):
            offset = i*30
            print "write=",dev.write(3, [COMMAND_GET_RESULT, offset%256, offset//256], interface=1)
            data = dev.read(129, 128, interface=1, timeout=50)
            values =data[4:]
            print values
            file.write(values)

    pass
"""

def setFreq(F):    
    print "write=",dev.write(3, struct.pack("=BI", COMMAND_SET_FREQUENCY, F), interface=1)
    readCommand()
    pass

def adcStart():
    dev.write(3, [COMMAND_ADC_START], interface=1)
    readCommand()
    pass

def adcElapsedTime():
    dev.write(3, [COMMAND_ADC_ELAPSED_TIME], interface=1)
    readCommand()
    pass

def adcReadBuffer():
    dev.write(3, [COMMAND_ADC_READ_BUFFER], interface=1)
    time.sleep(0.01)
    data = dev.read(129, 128, interface=1, timeout=50)
    size = struct.unpack_from('=I', data, 1)[0]

    print "adcReadBuffer size=", size

    result = None
    while size>0:
        data = dev.read(129, 128, interface=1, timeout=50)
        #print data
        size -= len(data)/2
        if not result:
            result = data
        else:
            result += data

    arr = array.array('H')
    arr.fromstring(result)
    #print arr
    return arr

def adcReadBufferAndSave():
    arr = adcReadBuffer()
    with open("out.dat", "wb") as file:
        arr.tofile(file)

def adcSynchro(inPeriod):
    print "adcStartSynchro=",dev.write(3, struct.pack("=BIB", COMMAND_START_SYNCHRO, inPeriod, 1), interface=1)
    data = dev.read(129, 128, interface=1, timeout=50)
    (period, clock, adc_tick) = struct.unpack_from('=III', data, 1)
    print "period=",period
    print "clock=",clock
    print "F=",clock/float(period)
    print "adc_tick=", adc_tick
    time.sleep(1)
    out = adcReadBuffer()
    with open("out.dat", "wb") as file:
        out.tofile(file)
    pass

def adcSynchro1(inPeriod):
    print "adcStartSynchro=",dev.write(3, struct.pack("=BIB", COMMAND_START_SYNCHRO, inPeriod, 1), interface=1)
    data = dev.read(129, 128, interface=1, timeout=50)
    (period, clock, adc_tick) = struct.unpack_from('=III', data, 1)
    print "period=",period, "clock=",clock , "F=",clock/float(period), "adc_tick=", adc_tick
    time.sleep(0.3)
    out = adcReadBuffer()

    result = smath.calcAll(period=period, clock=clock, adc_tick=adc_tick, data=out)
    return result

def allFreq():
    out = []

    with open("data.py", "wb") as file:
        P = 120000 #600.00 Hz
        #P = 7200 #10000.00 Hz
        #P = 3600 #20000.00 Hz
        PERIOD_ROUND120 = [P]*10
        for period in PERIOD_ROUND120:
            dev.write(3, [COMMAND_SET_LED, ord('0')], interface=1)
            readCommand()
            data = adcSynchro1(period)
            out.append(data)

            print>>file, 'ticks=', '{:3.2f}'.format(72000000*data['t_propagation']), 'fi=', data['fi']


def printEndpoint(e):
    print "Endpoint:"
    print "bLength=", e.bLength
    print "bDescriptorType=", e.bDescriptorType
    print "bEndpointAddress=", e.bEndpointAddress
    print "bmAttributes=", e.bmAttributes
    print "wMaxPacketSize=", e.wMaxPacketSize
    print "bInterval=", e.bInterval
    print "bRefresh=", e.bRefresh
    print "bSynchAddress=", e.bSynchAddress
    pass

def main():
    findDevice()
    dev.set_configuration()
    for cfg in dev:
        for i in cfg:
            print "interface=", i.bInterfaceNumber
            for e in i:
                print e.bEndpointAddress
                #printEndpoint(e)

    if True:
        #readOne()
        for x in xrange(3):
            print "write=",dev.write(3, [COMMAND_SET_LED, ord('0')], interface=1)
            readCommand()

    #setFreq(10000)
    #adcStart()

    freq = 600
    period = 72000000/freq
    #adcSynchro(period)
    allFreq()
    pass


main()

