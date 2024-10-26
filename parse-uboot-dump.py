#!/usr/bin/env python3
import re
import sys

infile = sys.argv[1]
outfile = sys.argv[2]

i = open(infile,"r")
o = open(outfile,"wb")

for line in i.readlines():
    line = line.strip()
    if re.match(r'^[0-9a-f]{8}:',line) or re.match(r'^0x[0-9a-f]{8}:',line):
        line = line.split(":")
        print(line)
        if len(line) == 2:
            line = line[1]
            line = line.replace("0x","")
            line = line.replace(" ","")[:32]
            data = bytes.fromhex(line)
            o.write(data)
