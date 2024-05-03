#!/usr/bin/env python3
from __future__ import absolute_import
import codecs
import os
import sys
import threading
import serial
from serial.tools.list_ports import comports
from serial.tools import hexlify_codec
import time
import re

try:
    raw_input
except NameError:
    # pylint: disable=redefined-builtin,invalid-name
    raw_input = input   # in python3 it's "raw"
    unichr = chr

if len(sys.argv) < 4:
    print(sys.argv[0]+" <mmc_dev:mmc_part> <device_file> <local_file>")
    sys.exit(1)

mmc_conf = sys.argv[1]
device_file = sys.argv[2]
local_file = sys.argv[3]

port = "/dev/ttyUSB0"
baudrate = 115200
databits = 8
stopbits = 1
parity = 'N'
rtscts = False
xonxoff = False
rts = None
dtr = None
exclusive = False
echo = False
eol='CRLF'
raw = False
filters = ['default']
serial_port_encoding = 'UTF-8'
quiet = False

s = serial.serial_for_url(
    port,
    baudrate,
    timeout=.1,
    bytesize=databits,
    parity=parity,
    stopbits=stopbits,
    rtscts=rtscts,
    xonxoff=xonxoff,
    do_not_open=True)

s.dtr = dtr
s.rts = rts
s.exclusive = exclusive
s.open()

# LOAD CMD
cmd = 'ext4load mmc ' + mmc_conf + ' 0xc2600000 ' + device_file + '\n'
print("CMD: "+ cmd.strip())
s.write(cmd.encode('utf-8'))
s.flush()
time.sleep(5)

# LOAD CMD RESP
out = bytes()
while s.inWaiting() > 0:
    out += s.read(1)
out = out.decode("utf-8")
print("RESP: "+ out)

# PARSE READ SIZE
size = 0
try:
    size = int(re.search("[0-9]+ bytes read", out).group(0)[:-11])
except:
    sys.exit(1)
print("READ SIZE: " + str(size))

# MEMORY READ CMD
cmd = 'md.b 0xc2600000 ' + hex(size) + '\r\n'
print("CMD: " + cmd.strip())
s.write(cmd.encode('utf-8'))

# MEMORY READ CMD RESP
out = bytes()
while 1:
    # read all that is there or wait for one byte
    o = s.read(s.in_waiting or 1)
    out += o
    if len(o) == 0:
        break

# PARSE MEMORY READ
rawdata = bytes()
for line in out.decode("utf-8").split("\r\n"):
    try:
        d = re.search(r'([0-9a-f])+: ([0-9a-f]{2}\s)+', line).group(0)
        d = bytes.fromhex(re.search(r'([0-9a-f]{2}\s)+', d).group(0).replace(" ",""))
        rawdata += d
    except:
        pass

# WRITE FILE TO STDOUT
#print()
#print("================ FILE CONTENTS ================")
#sys.stdout.buffer.write(rawdata)

# WRITE FILE TO LOCAL FILE
f = open(local_file,'wb')
f.write(rawdata)

s.close()

