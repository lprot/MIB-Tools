import os, re

#Format: name of the patch, search pattern, offset, patch
patches = ['SWaP signature check', b'\x00\x00\x50\xE3\x8D\x00\x00\x1A', 0, b'\x01\x00\xA0\xE3\x8D\x00\x00\xEA',
           'VCRN matching check', b'\x00\x00\x54\xE3\x55\x00\x00\x1A', 0, b'\x01\x40\xA4\xE3\x55\x00\x00\xEA',
           'Exception list signature check', b'\xEB\x00\x00\x50\xE3\x8A\x00\x00\x0A', 1, b'\x07',
           'Setting RPMB key check', b'\xEB\x00\x00\x50\xE3\x25\x00\x00\x0A', 1, b'\x07']

f = open('tsd.mibstd2.system.swap', 'rb')
data = f.read()
f.close()

f = open("tsd.mibstd2.system.swap.patched", 'w+b')
f.write(data)
flog = open("tsd.mibstd2.system.swap.patchlog.txt", 'w')

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