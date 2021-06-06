import sys
if sys.version_info[0] < 3:
    raw_input("You need to run this with Python 3!\nPress Enter to exit...")
    sys.exit(1)

import os, re

#Format: name of the patch, search pattern, offset, patch
patches = ['metainfo2.txt signature (aSignatureOfMet) check', b'\x00\x00\x50\xE3\x15\x00\x00\x0A\x54\x17\x9F\xE5', 0, b'\x07',
           'metainfo2.txt checksum (aParseErrorInva_1) check', b'\xE3.\xFD\xFF\x1A..\x1F\xE5', 4, b'\xEA',
           'metainfo2.txt signature (aParseErrorInva_0) check', b'\x1B\x00\x00\x1A..\x1F\xE5', 3, b'\xEA',
           'Dependencies of update not met (aDependenciesOf) check', b'..\xFD\xEB\x00\x00\x50\xE3\x30\x00\x00\x1A', 4, b'\x07']

f = open('tsd.mibstd2.system.swdownload', 'rb')
data = f.read()
f.close()

f = open("tsd.mibstd2.system.swdownload.patched", 'w+b')
f.write(data)
flog = open("tsd.mibstd2.system.swdownload.patchlog.txt", 'w')

num_of_applied_patches = 0
num_of_patches = int(len(patches)/4)
for i in range(num_of_patches):
  search_pattern = patches[i * 4 + 1]
  for match in re.compile(search_pattern).finditer(data):
   offset = match.start()
   length = match.end() - offset
   f.seek(offset)
   oldbytes = f.read(length)
   newbytes = oldbytes[0:patches[i * 4 + 2]] + patches[i * 4 + 3] + oldbytes[len(patches[i * 4 + 3]) + patches[i * 4 + 2]:length]
   print(patches[i * 4] + ' found at ' + hex(offset).upper().replace('0X', '0x') + '. Changing ' + oldbytes.hex().upper() + ' to ' + newbytes.hex().upper())
   flog.writelines(hex(offset).upper().replace('0X', '0x') + ': ' + oldbytes.hex().upper() + ' ' + newbytes.hex().upper() + '\n')
   num_of_applied_patches += 1
   f.seek(offset)
   f.write(newbytes)
f.close()

if num_of_patches == num_of_applied_patches:
 print('\nAll patches are applied :)')
else:
 print('\nWARNING! Not all patches are applied!')

input("\nPress Enter to exit...")