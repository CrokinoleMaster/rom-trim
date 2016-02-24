#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, io, struct
import hashlib

print "checksuming {}".format(sys.argv[1])
rom = io.open(sys.argv[1], "rb")
rom.seek(0x100)
assert rom.read(4).decode("ascii") == "NCSD"
fullsize = struct.unpack("<I",rom.read(4))[0] << 9
rom.seek(0x300)
trimsize = struct.unpack("<I",rom.read(4))[0]
rom.seek(0)
md5 = hashlib.md5()
sha1 = hashlib.sha1()
while rom.tell() < trimsize:
    data = rom.read1(min(1<<16,trimsize-rom.tell()))
    md5.update(data)
    sha1.update(data)
omd5=md5.copy()
osha1=sha1.copy()
for data in rom:
    omd5.update(data)
    osha1.update(data)
rom.close()
print "current MD5    : {}".format(omd5.hexdigest())
print "current SHA1   : {}".format(osha1.hexdigest())
print "trimmed MD5    : {}".format(md5.hexdigest())
print "trimmed SHA1   : {}".format(sha1.hexdigest())
md5.update("\xff"*(fullsize-trimsize))
sha1.update("\xff"*(fullsize-trimsize))
print "untrimmed MD5  : {}".format(md5.hexdigest())
print "untrimmed SHA1 : {}".format(sha1.hexdigest())
