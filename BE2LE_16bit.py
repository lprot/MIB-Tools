import sys
chunk = open(sys.argv[1], "rb").read()
converted = bytearray([])
for i in range(int(len(chunk)/2)):
   converted += bytearray([ chunk[i*2+1], chunk[i*2] ])

open(sys.argv[2] , "wb").write(converted)