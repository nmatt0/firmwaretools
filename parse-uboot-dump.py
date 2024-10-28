#!/usr/bin/env python3
#
# 20241026 original from matt brown, modified by jens heine <binbash@gmx.net>
#
import os
import re
import sys
from optparse import OptionParser
from pathlib import Path


# def decode_2_ascii(b: bytes) -> str:
#     result_str = ""
#     for _b in list(b):
#         if int.from_bytes(_b, "little") >= 32 and int.from_bytes(_b) <= 126:
#             result_str = result_str + chr(int.from_bytes(_b))


def main():
    parser = OptionParser()
    parser.add_option("-i", "--infile", dest="infile",
                      help="read data from FILE (required)", metavar="FILE")
    parser.add_option("-o", "--outfile", dest="outfile",
                      help="write binary data to FILE (default: firmware.bin)", metavar="FILE")
    parser.add_option("-l", "--little-endian", dest="little_endian",
                      help="convert data to little endian (default:big endian)", action="store_true")
    parser.add_option("-f", "--force", dest="force",
                      help="force overwrite existing outfile", action="store_true")
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

    _little_endian = False
    if options.little_endian:
        _little_endian = options.little_endian

    _force = False
    if options.force:
        _force = options.force

    _verbose = False
    if options.verbose:
        _verbose = options.verbose

    if not _force and Path(outfile).is_file():
        print("Error: outfile '" + str(outfile) + "' already exists.")
        answer = input("Overwrite (y/N)? : ")
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
            if len(line) == 2:
                line = line[1]
                line = line.replace("0x", "")
                memory_address_contents = line.split(" ")
                for memory_address_content in memory_address_contents:
                    if len(memory_address_content) == 0:
                        continue
                    if _verbose:
                        try:
                            decoded = bytes.fromhex(memory_address_content).decode(encoding="ascii")
                        except:
                            decoded = '..'
                        print('Offset in  : ' + str(data_count).rjust(8) + ' ' + str(memory_address_content)
                              + ' : ' + decoded)
                    if _little_endian:
                        memory_address_content = (memory_address_content[2:4] + memory_address_content[0:2]
                                                  + memory_address_content[6:8] + memory_address_content[4:6])
                    data = bytes.fromhex(memory_address_content)
                    # if len(data) == 0:
                    #     continue
                    if _verbose:
                        try:
                            decoded = bytes.fromhex(memory_address_content).decode(encoding="ascii")
                        except:
                            decoded = '..'
                        print('Offset out : ' + str(data_count).rjust(8) + ' ' + str(memory_address_content)
                              + ' : ' + decoded)
                    o.write(data)
                    data_count += len(data)
    print()
    print(str(data_count) + ' bytes written to ' + outfile)


if __name__ == '__main__':
    main()
