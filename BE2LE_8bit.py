import os, sys, hashlib
import struct

infile = sys.argv[1]
outfile = sys.argv[2]

with open(infile, "rb") as old, open(outfile , "wb") as new:
    for chunk in iter(lambda: old.read(4), b""):
        chunk = struct.pack("<f", struct.unpack(">f", chunk)[0])
        new.write(chunk)