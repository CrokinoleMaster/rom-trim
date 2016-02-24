#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, io, struct

print "untrimming {}".format(sys.argv[1]),
rom = io.open(sys.argv[1], "rb+")
rom.seek(0x100)
assert rom.read(4).decode("ascii") == "NCSD"
fullsize = struct.unpack("<I",rom.read(4))[0] << 9
rom.seek(0x300)
trimsize = struct.unpack("<I",rom.read(4))[0]
rom.seek(trimsize)
assert rom.read1(1<<8) == ""
assert rom.tell() == trimsize
while rom.tell() < fullsize:
    rom.write("\xff"*min(1<<16,fullsize-rom.tell()))
rom.close()
print "to {:,} Bytes".format(fullsize)
