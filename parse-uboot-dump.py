#!/usr/bin/env python3
#
# 20241026 original from matt brown, modified by jens heine <binbash@gmx.net>
#
import re
import sys
from optparse import OptionParser


def main():
    parser = OptionParser()
    parser.add_option("-i", "--infile", dest="infile",
                      help="read data from FILE", metavar="FILE")
    parser.add_option("-o", "--outfile", dest="outfile",
                      help="write binary data to FILE", metavar="FILE")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="be verbose")

    (options, args) = parser.parse_args()

    infile = None
    if options.infile:
        infile = options.infile

    outfile = None
    if options.outfile:
        outfile = options.outfile

    if infile is None or outfile is None:
        print("Error: Missing argument, try -h for help")
        sys.exit(1)

    _verbose = False
    if options.verbose:
        _verbose = options.verbose

    i = open(infile, "r")
    o = open(outfile, "wb")

    for line in i.readlines():
        line = line.strip()
        if re.match(r'^[0-9a-f]{8}:', line) or re.match(r'^0x[0-9a-f]{8}:', line):
            line = line.split(":")
            if _verbose:
                print(line)
            if len(line) == 2:
                line = line[1]
                line = line.replace("0x", "")
                line = line.replace(" ", "")[:32]
                data = bytes.fromhex(line)
                o.write(data)


if __name__ == '__main__':
    main()
