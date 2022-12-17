#-------------------------------------------------------------------------------
#--- Quick 'n' dirty nds2sqlite converter
#
# Author: lprot
# Version: 1
# Zipfs description: https://www.sqlite.org/zipvfs/doc/trunk/www/fileformat.wiki
#-------------------------------------------------------------------------------
import sys

if sys.version_info[0] < 3:
    raw_input("You need to run this with Python 3!\nPress Enter to exit...")
    sys.exit(1)

import os, struct, zlib

def convert(filename, out_dir):
    print("\nReading %s..." % filename)
    data = open(filename, 'rb').read()
    (dataStart,) = struct.unpack_from('>Q', data, 108)
    (dataEnd,) = struct.unpack_from('>Q', data, 116)
    (dbSize,) = struct.unpack_from('>Q', data, 140)
    (pageSize,) = struct.unpack_from('>I', data, 172)
    (version,) = struct.unpack_from('>I', data, 176)
    print("\nZV-zlib header: dataStart=0x%lX, dataEnd=0x%lX, dbSize=%d, pageSize=0x%lX, version=%d" % (dataStart, dataEnd, dbSize, pageSize, version))
    offset = 200
    (page_entry,) = struct.unpack_from('>Q', data, offset)
    encrypted = 0
    sqlite = open(os.path.splitext(filename)[0] + '.sqlite', 'wb')
    print('Parsing the Page-Map at offset 0x%lX...' % offset)
    while offset < dataStart: 
        page_offset = page_entry >> 24 # bits 24-63 (40 bits)
        page_size = (page_entry & 0xFFFF80) >> 7 # bits 7-23 (17 bits)
        page_unusedBytes = page_entry & 0x7F # bits 0-6 (7 bits)
        if page_entry != 0 and page_offset != 0:
            print("page_entry=%lX, page_offset=0x%lX, page_size=0x%lX, page_unusedBytes=%d" % (page_entry, page_offset, page_size, page_unusedBytes))
            (slot_header,) = struct.unpack_from('>Q', data, page_offset)
            page_number = slot_header >> 33 # bits 33-63 (31 bit)
            slot_payload_size = (slot_header & 0x1FFFF0000) >> 16 # bits 16-32 (17 bits)
            compression_type = slot_header & 0xFFFF # bits 0-15 (first 2 bytes of the payload)
            if compression_type == 0x789C and not encrypted:
                sqlite.write(zlib.decompress(data[page_offset+6:page_offset+6+slot_payload_size]))
                encrypted = ''
            else:
                encrypted = ' (encrypted/unknown)'
            print("page_number=%d, slot_payload_size=0x%lX, compression_type=0x%lX%s" % (page_number, slot_payload_size, compression_type, encrypted))
            #print(data[page_offset+6:page_offset+6+slot_payload_size])
        offset += 8
        (page_entry,) = struct.unpack_from('>Q', data, offset)
    if sqlite.tell() == dbSize:
        print('Successfully converted. The size of ' + os.path.splitext(filename)[0] + '.sqlite' + ' matches dbSize ;)')
    else: 
        if sqlite.tell() == 0: 
            print('Coversion failed. The file is encrypted!')
        else:
            print("Something went wrong: sqlite size doesn't match dbSize!")
    sqlite.close()

match len(sys.argv):
    case 2:
        convert(sys.argv[1], '.\\' + os.path.splitext(sys.argv[1])[0])
    case 1:
        for filename in os.scandir('.\\'):
            if filename.is_file() and (filename.name.endswith('.nds') or filename.name.endswith('.NDS') or filename.name.endswith('.db')):
                convert(filename.name, os.path.splitext(filename)[0])
    case _:
        print("Usage: nds2sqlite.py <filename>")
        print("   or: nds2sqlite.py")
        input("\nPress Enter to exit...")
        sys.exit(1)

input("\nPress Enter to exit...")
sys.exit(1)