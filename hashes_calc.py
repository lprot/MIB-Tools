import os, sys, hashlib 

if os.path.sep == "\\":
  eol = '\n'
else:
  eol = '\r\n'

fout = open('hashes.txt','w')
for dirpath, dirs, files in os.walk('tsd'):
  for filename in files:
    fname = os.path.join(dirpath,filename)
    with open(fname, 'rb') as f:
      if fout.tell():
        fout.write(eol + eol)
      fout.write('FileName = "/' + fname.replace(os.path.sep, '/') + '"' + eol)
      fout.write('FileSize = "' + str(os.stat(fname).st_size) + '"' + eol)
      sha1 = hashlib.sha1()
      while True:
        data = f.read(65536) #BUF_SIZE
        if not data:
         break
        sha1.update(data)
      fout.write('Checksum = "' + sha1.hexdigest() + '"')
if fout.tell():
 print('hashes.txt is recalculated :)')
else:
 print('Something went wrong :(')
fout.close()