# firmwaretools
a set of scripts and tools for various firmware analysis tasks

## parse-uboot-dump.py

parse-uboot-dump.py - Use this tool to parse the picocom output of a uboot memory dump and create a firmware.bin file from it. There is also little endian support (needed for fritz 7141 i.e.). I reccomend to create a binary from the parse-uboot-dump.py with: 

```
pyinstaller parse-uboot-dump.py --onefile --clean
```
You can find the static binary in the ./dist folder which I use in the following example.

Let's say we dump some memory data like this from the uboot prompt and we have captured the output :

```
picocom -b 38400 -l -r /dev/ttyUSB0 --logfile `date +"%Y%m%d_%H%M%S"`_picocom.log
...

Eva_AVM >dm 0x90010000 100

0x90010000: 0xFEED1281 0x000A7B78 0x94000000 0x075A0201
0x90010010: 0x000A7B60 0x0020B085 0x00AEE9B1 0x8000005D
0x90010020: 0x00000000 0xFD6F0000 0xB7A3FFFF 0xE9FF4581
0x90010030: 0x21F14485 0xBB6544E2 0x34D6C2AC 0x088E0F7B
0x90010040: 0x3E009DD3 0x66CD578E 0xEA57F680 0x779805D8
0x90010050: 0xFBF3D43C 0x2BFFCC97 0x1E6DFDC2 0x491DA9F2
0x90010060: 0x0387B70D 0xEA8EF4BD 0x078A3680 0xC9BF1778
0x90010070: 0x7BC23E02 0xA9985FE5 0x037D49E0 0x93238AC1
0x90010080: 0x3235276B 0x64687BAF 0x6BD2204E 0x91A30B23

```

```
parse-uboot-dump -h
Usage: parse-uboot-dump [options]

Options:
  -h, --help            show this help message and exit
  -i FILE, --infile=FILE
                        read data from FILE (required)
  -o FILE, --outfile=FILE
                        write binary data to FILE (default: firmware.bin)
  -l, --little-endian   convert data to little endian (default:big endian)
  -f, --force           force overwrite existing outfile
  -v, --verbose         be verbose
```

We can now parse the picocom output and convert it to a nice firmware.bin file which has the correct little endian mapping already done:

```
parse-uboot-dump -i 20241026_232645_picocom.log -l
```
Now you can nicely binwalk through the binary "firmware.bin"...

Happy coding, Jens
