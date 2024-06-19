#!/usr/bin/env python3
import re
import sys

infile = sys.argv[1]
outfile = sys.argv[2]

i = open(infile,"r")
o = open(outfile,"wb")

for line in i.readlines():
    line = line.strip()
    line = ''.join(char for char in line if ord(char) < 128 and ord(char) != 0)
    if re.match(r'^[0-9a-f]{8}:',line):
        line = line.split(":")
        if len(line) > 1:
            line = line[1]
            line = line.replace(" ","")[:32]
            data = bytes.fromhex(line)
            o.write(data)
