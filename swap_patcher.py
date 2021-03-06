import sys
if sys.version_info[0] < 3:
    raw_input("You need to run this with Python 3!\nPress Enter to exit...")
    sys.exit(1)
    
import os, re

#Format: name of the patch, search pattern, offset, patch
patches = ['Setting the RPMB key failed check', b'\\xEB\\x00\\x00\\x50\\xE3\\x25\\x00\\x00\\x0A\\x54', 1, b'\x07',
           'Signature of exception list is invalid check', b'\\xEB\\x00\\x00\\x50\\xE3\\x8A\\x00\\x00\\x0A', 1, b'\x07',
           'Signature is invalid check', b'\\x00\\x00\\x50\\xE3\\x8D\\x00\\x00\\x1A', 0, b'\x07',
           'VCRN of FEC does not match check', b'\\x00\\x00\\x54\\xE3\\x55\\x00\\x00\\x1A', 0, b'\x07',
           'signature is invalid check (1xx)', b'\\xEB\\x00\\x00\\x50\\xE3\\x74\\x00\\x00\\x1A', 1, b'\x07',
           'VCRN of FEC does not match check (1xx)', b'\\x00\\x00\\x54\\xE3\\xB4\\x00\\x00\\x1A', 0, b'\x07',
           'Setting the RPMB key failed check (1xx)', b'\\xEB\\x00\\x00\\x50\\xE3\\x21\\x00\\x00\\x0A\\x11', 1, b'\x07',
           'Signature of exception list is invalid check (1xx)', b'\\x00\\x00\\x50\\xE3\\x22\\x00\\x00\\x1A\\x2F', 0, b'\x07',
           'Signature of exception list is invalid check (patched)', b'\\xEB\\x00\\x00\\x50\\xE3\\x8A\\x00\\x00\\x1A\\xB8', 8, b'\xE3',
           'Setting the RPMB key failed check (mainstd)', b'\\xEB\\x00\\x00\\x50\\xE3\\x3C\\x10\\x84\\xE2\\x13', 1, b'\x07',
           'Signature of exception list is invalid check (mainstd)', b'\\x00\\x00\\x50\\xE3\\x15\\x00\\x00\\x1A...\\xE2...\\xE1', 0, b'\x07',
           'signature is invalid check (mainstd)', b'\\x2F\\x4B\\xE2...\\xEB\\x00\\x00\\x50\\xE3.\\x00\\x00\\x1A', 7, b'\x07',
           'VCRN of FEC does not match check (mainstd)', b'\\xFF\\xEA\\x00\\x00\\x54\\xE3.\\x00\\x00\\x1A', 2, b'\x07']

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

if num_of_applied_patches >= 3:
 print('\nAll patches are applied :)')
else:
 print('\nWARNING! Not all patches are applied!')
 
input("\nPress Enter to exit...")