import sys

infile = sys.argv[1]
outfile = sys.argv[2]

a = open(infile, "rb")
chunk = a.read()
converted = bytearray([])
for i in range(int(len(chunk)/2)):
   converted += bytearray([ chunk[i*2+1], chunk[i*2] ])

b = open(outfile , "wb")
b.write(converted)
b.close()
a.close()
