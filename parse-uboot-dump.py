#!/usr/bin/env python3
#
# 20241026 original from matt brown, modified by jens heine <binbash@gmx.net>
#
import os
import re
import sys
from optparse import OptionParser
from pathlib import Path


def main():
    parser = OptionParser()
    parser.add_option("-i", "--infile", dest="infile",
                      help="read data from FILE (required)", metavar="FILE")
    parser.add_option("-o", "--outfile", dest="outfile",
                      help="write binary data to FILE", metavar="FILE")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="be verbose")

    (options, args) = parser.parse_args()

    infile = None
    if options.infile:
        infile = options.infile

    outfile = "firmware.bin"
    if options.outfile:
        outfile = options.outfile

    if infile is None:
        print("Error: Missing argument, try -h for help")
        sys.exit(1)

    _verbose = False
    if options.verbose:
        _verbose = options.verbose

    if Path(outfile).is_file():
        print("Error: outfile already exists.")
        answer = input("Overwrite (y/n)? : ")
        print()
        if answer != 'y':
            sys.exit(0)
        else:
            os.remove(outfile)

    i = open(infile, "r")
    o = open(outfile, "wb")

    data_count = 0
    for line in i.readlines():
        line = line.strip()
        if re.match(r'^(0x)*[0-9A-Fa-f]{8}:', line):
            line = line.split(":")
            #if _verbose:
            #    print('in  : ' + str(line))
            if len(line) == 2:
                line = line[1]
                line = line.replace("0x", "")
                line = line.replace(" ", "")[:32]
                data = bytes.fromhex(line)
                if _verbose:
                    #print('out : ' + line)
                    print(str(line))
                o.write(data)
                data_count += len(data)
    print()
    print(str(data_count) + ' bytes written to ' + outfile)


if __name__ == '__main__':
    main()
