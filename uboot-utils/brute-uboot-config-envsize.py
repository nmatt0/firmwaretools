#!/usr/bin/env python3

import argparse
import zlib
import sys

def main():
    try:
        parser = argparse.ArgumentParser(
            prog='brute-uboot-config-envsize',
            description='guesses the CONFIG_ENV_SIZE of a U-Boot ENV given an offset'
        )
        parser.add_argument('offset', nargs=1, help='offset of U-Boot ENV in the current file')
        parser.add_argument('file', nargs=1, help='firmware file containing U-Boot ENV')
        #parser.print_help()
        args = parser.parse_args()
        
        # parse int as decimal or hex
        offset = args.offset[0]
        if offset.startswith("0x"):
            offset = int(offset.replace("0x", ""),16)
        else:
            offset = int(offset)
        file = args.file[0]

        f = open(file,'rb')
        f.seek(offset)

        # https://github.com/u-boot/u-boot/blob/82b69fc4224432d5aefa7ca750d950374cbc7fb2/include/env_internal.h#L62C19-L62C34
        # ENV_SIZE (CONFIG_ENV_SIZE - ENV_HEADER_SIZE)
        # ENV_HEADER_SIZE is 4 bytes
        crc = f.read(4)
        crc_i = int.from_bytes(crc, byteorder='little')

        uboot_data = b""
        while True:
            uboot_data += f.read(1)
            calc_crc = zlib.crc32(uboot_data)
            if crc_i == calc_crc:
                size = len(uboot_data) + 4
                print("CONFIG_ENV_SIZE: " + str(hex(size)))
                break
            if len(uboot_data) > 0x100000:
                print("Failed to find CONFIG_ENV_SIZE")
                break
        #print("current CRC32: "+current_crc.hex())
        #print("calculated CRC32: "+crc.to_bytes(4, 'little').hex())
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
