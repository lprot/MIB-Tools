import sys, struct
with open(sys.argv[1], "rb") as old, open(sys.argv[2] , "wb") as new:
    for chunk in iter(lambda: old.read(4), b""):
        chunk = struct.pack("<I", struct.unpack(">I", chunk)[0])
        new.write(chunk)