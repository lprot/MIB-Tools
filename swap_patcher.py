import sys
if sys.version_info[0] < 3:
    raw_input("You need to run this with Python 3!\nPress Enter to exit...")
    sys.exit(1)
    
import os, re

#Format: name of the patch, search pattern, offset, patch
patches = ['Setting RPMB key check', b'\\xEB\\x00\\x00\\x50\\xE3\\x25\\x00\\x00\\x0A\\x54', 1, b'\\x07',
           'Exception list signature check', b'\\xEB\\x00\\x00\\x50\\xE3\\x8A\\x00\\x00\\x0A', 1, b'\\x07',
           'SWaP signature check', b'\\x00\\x00\\x50\\xE3\\x8D\\x00\\x00\\x1A', 0, b'\\x07',
           'SWaP signature check fw1xx', b'\\xEB\\x00\\x00\\x50\\xE3\\x74\\x00\\x00\\x1A', 1, b'\\x07',
           'VCRN matching check fw1xx', b'\\x00\\x00\\x54\\xE3\\xB4\\x00\\x00\\x1A', 0, b'\\x07',
           'Setting RPMB key check fw1xx', b'\\xEB\\x00\\x00\\x50\\xE3\\x21\\x00\\x00\\x0A\\x11', 1, b'\\x07',
           'Exception list signature check fw1xx', b'\\x00\\x00\\x50\\xE3\\x22\\x00\\x00\\x1A\\x2F', 0, b'\\x07',
           'VCRN matching check', b'\\x00\\x00\\x54\\xE3\\x55\\x00\\x00\\x1A', 0, b'\\x07',
           'Exception list signature check CN', b'\\xEB\\x00\\x00\\x50\\xE3\\x8A\\x00\\x00\\x1A\\xB8', 8, b'\\xE3']

f = open('tsd.mibstd2.system.swap', 'rb')
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
   
f = open("tsd.mibstd2.system.swap.patched", 'w+b')
f.write(data)
f.close()

if num_of_patches == num_of_applied_patches:
 print('\nAll patches are applied :)')
else:
 print('\nWARNING! Not all patches are applied!')
 
input("\nPress Enter to exit...")