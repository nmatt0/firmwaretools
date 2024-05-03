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

if len(sys.argv) < 3:
    print(sys.argv[0]+" <mmc_dev:mmc_part> <device_file>")
    sys.exit(1)

mmc_conf = sys.argv[1]
device_file = sys.argv[2]

device = "/dev/ttyUSB0"
baud = 115200

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

cmd = b'ext4ls mmc ' + mmc_conf.encode('utf-8') + b' ' + device_file.encode('utf-8') + b'\n'
s.write(cmd)
#s.flush()
time.sleep(1)
out = bytes()
while s.inWaiting() > 0:
    out += s.read(1)
out = out.decode("utf-8")
print(out)
s.close()
