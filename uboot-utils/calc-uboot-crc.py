#!/usr/bin/env python3

import argparse
import zlib
import sys

def main():
    try:
        parser = argparse.ArgumentParser(
            prog='uboot-crc-calc',
            description='calculates the CRC32 of a U-Boot ENV given an offset and CONFIG_ENV_SIZE'
        )
        parser.add_argument('offset', nargs=1, help='offset of U-Boot ENV in the current file')
        parser.add_argument('size', nargs=1, help='U-Boot CONFIG_ENV_SIZE')
        parser.add_argument('file', nargs=1, help='firmware file containing U-Boot ENV')
        #parser.print_help()
        args = parser.parse_args()
        
        # parse int as decimal or hex
        offset = args.offset[0]
        if offset.startswith("0x"):
            offset = int(offset.replace("0x", ""),16)
        else:
            offset = int(offset)
        size = args.size[0]
        if size.startswith("0x"):
            size = int(size.replace("0x", ""),16)
        else:
            size = int(size)
        file = args.file[0]

        f = open(file,'rb')
        f.seek(offset)

        # https://github.com/u-boot/u-boot/blob/82b69fc4224432d5aefa7ca750d950374cbc7fb2/include/env_internal.h#L62C19-L62C34
        # ENV_SIZE (CONFIG_ENV_SIZE - ENV_HEADER_SIZE)
        # ENV_HEADER_SIZE is 4 bytes
        current_crc = f.read(4)
        uboot_data = f.read(size-4)

        crc = zlib.crc32(uboot_data)
        print("current CRC32: "+current_crc.hex())
        print("calculated CRC32: "+crc.to_bytes(4, 'little').hex())
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
