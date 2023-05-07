import sys
if sys.version_info[0] < 3:
    raw_input("You need to run this with Python 3!\nPress Enter to exit...")
    sys.exit(1)

import os, hashlib 

if os.path.sep == "\\":
    eol = '\n'
else:
    eol = '\r\n'

if len(sys.argv) < 2 and not os.path.exists('tsd'):
    print("ERROR: Cannot find tsd folder!")
    print(eol + "Usage: hash_calc.py <filename>")
    input(eol +"Press Enter to exit...")
    sys.exit(1)

fout = open('hashes.txt','w')
folder = 'tsd'
if len(sys.argv) > 1:
    folder = sys.argv[1]
for dirpath, dirs, files in os.walk(folder):
  for filename in files:
    fname = os.path.join(dirpath,filename)
    with open(fname, 'rb') as f:
        if fout.tell():
            fout.write(eol)
        fout.write('FileName = "/' + fname.replace(os.path.sep, '/') + '"' + eol)
        fout.write('FileSize = "' + str(os.stat(fname).st_size) + '"' + eol)
        i=0
        while True:
            data = f.read(524288) #BUF_SIZE
            if not data: break
            sha1 = hashlib.sha1()
            sha1.update(data)
            if i > 0: n = str(i)
            else: n =''
            fout.write('Checksum'+ n + ' = "' + sha1.hexdigest() + '"' + eol)
            i+=1
if fout.tell():
    input('hashes.txt is recalculated :)' + eol + eol + "Press Enter to exit...")
else:
    input('Something went wrong :(' + eol + eol + "Press Enter to exit...")
fout.close()