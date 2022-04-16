import sys
if sys.version_info[0] < 3:
    raw_input("You need to run this with Python 3!\nPress Enter to exit...")
    sys.exit(1)

import os, re

#Format: name of the patch, search pattern, offset, patch
patches = ['metainfo2.txt signature (aSignatureOfMet) check', b'.\\x00\\x56\\xE3\\x7D\\x00\\x00\\x0A\\x52\\x0F\\x4B\\xE2', 0, b'\x07',
           'metainfo2.txt signature (aParseErrorInva_0) check', b'.\\x00\\x54\\xE3\\x1B\\x00\\x00...\\x1F\\xE5', 0, b'\x07',
           'metainfo2.txt checksum (aParseErrorInva_1) check', b'.\\x00\\x50\\xE3.\\xFD\\xFF...\\x1F\\xE5', 0, b'\x07',
           'Dependencies of update not met (aDependenciesOf) check', b'..\\xFD\\xEB.\\x00\\x50\\xE3\\x30\\x00\\x00\\x1A\\x04\\x00', 4, b'\x07',
           'metainfo2.txt signature (aSignatureOfMet) check fw1xx', b'\\x00\\x00\\x53\\xE3\\x19\\x00\\x00\\x0A\\x52\\x0E\\x4B\\xE2', 0, b'\x07',
           'metainfo2.txt signature (aParseErrorInva_0) check fw1xx', b'\\x00\\x00\\x54\\xE3\\x29\\x00\\x00\\x1A\\x5C\\x14\\x9F\\xE5', 0, b'\x07',
           'metainfo2.txt signature (aParseErrorInva_1) check fw1xx', b'\\x00\\x00\\x50\\xE3\\x2D\\xFE\\xFF\\x1A\\x54\\x13\\x9F\\xE5', 0, b'\x07']

f = open('tsd.mibstd2.system.swdownload', 'rb')
data = bytearray(f.read())
print('File size:', f.tell(), 'bytes')
f.close()

num_of_applied_patches = 0
num_of_patches = int(len(patches)/4)
for i in range(num_of_patches):
  search_pattern = patches[i * 4 + 1]
  for match in re.compile(search_pattern).finditer(data):
   offset = match.start() + patches[i * 4 + 2]
   print(patches[i * 4] + ' found at ' + hex(offset).upper().replace('0X', '0x'))
   for j in range(len(patches[i * 4 + 3])):
    data[offset + j] = patches[i * 4 + 3][j]
   num_of_applied_patches += 1

f = open("tsd.mibstd2.system.swdownload.patched", 'w+b')
f.write(data)
f.close()

if num_of_applied_patches >= 3:
 print('\nAll patches are applied :)')
else:
 print('\nWARNING! Not all patches are applied!')

input("\nPress Enter to exit...")