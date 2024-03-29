#-------------------------------------------------------------------
#--- startScript_x.anim images extractor
#
# Author:      Jille, lprot
# Revision:    3
# Changelog:   1: Initial version
#              2: BGRA to RGBA conversion to prevent red R-lines ;-)
#              3: Automatisation of routine operations
#-------------------------------------------------------------------
import sys

if sys.version_info[0] < 3:
    raw_input("You need to run this with Python 3!\nPress Enter to exit...")
    sys.exit(1)

import os, struct, zlib
try:
    from PIL import Image
except ImportError:
    print("  You are missing the PIL module!\n"
          "  install it by running:\n"
          "  pip install image")
    input("\nPress Enter to exit...")
    sys.exit(1)

def extract(filename, out_dir):
    if not os.path.exists(out_dir):
      os.mkdir(out_dir)

    data = open(filename,'rb').read()
    offset = 0
    filesize = sys.getsizeof(data)
    print("\nOpened %s. Size: %d bytes" %(filename, filesize))

    (magic,) = struct.unpack_from('<8s', data, offset)
    offset += 12
    (cmd_block_len,) = struct.unpack_from('<L', data, offset)
    offset += cmd_block_len + 16
    (number_of_files,) = struct.unpack_from('<L', data, offset)
    print ("Command block length: %d. Number of files: %d" %(cmd_block_len, number_of_files))

    # extracting command list
    cmd_offset = 20
    i = 0
    num_blocks = cmd_block_len / 32
    print("Number of commands in command list: %d. Extracting to animation_script.csv..." % num_blocks)
    f_commands = open(os.path.join(out_dir, 'animation_script.csv'), 'wt')
    while i < num_blocks:
        (nn,cmd,arg1,arg2,arg3,arg4,arg5,arg6) = struct.unpack_from('<IIIIIIII', data, cmd_offset)
        match cmd:
            case 0:
                comment = 'BEGIN'
            case 1:
                comment = 'END'
            case 2:
                comment = 'CLEAR SCREEN'
            case 3:
                comment = 'SET RESOLUTION '+str(arg3).zfill(2)+'x'+str(arg4)
            case 4:
                comment = 'DRAW img_'+str(arg1).zfill(2)+' at x='+str(arg3)+', y='+str(arg4)
            case 5:
                comment = 'DRAW STICKER img_'+str(arg1).zfill(2)+' at x='+str(arg3)+', y='+str(arg4)
            case 6:
                comment = 'WAIT '+str(arg1*0.01)+' sec.'
            case 7:
                comment = 'START/END ANIMATION'
            case 10:
                comment = 'IF STICKER='+str(arg2)+' THEN'
            case 11:
                comment = 'ELSE'
            case 12:
                comment = 'ENDIF'
            case _:
                comment = 'UNKNOWN'
        f_commands.write("{};{};{};{};{};{};{};{};{}\n".format(nn,cmd,arg1,arg2,arg3,arg4,arg5,arg6,comment).replace("4294967295",""))
        cmd_offset += 32
        i += 1
    f_commands.close()

    #extracting images
    i = j = 0
    offset += 4
    offsets_array = []

    #fill offsets+array
    while (i < number_of_files):
        (file_offset,) = struct.unpack_from('<L', data, offset)
        offsets_array.append(file_offset)
        offset += 4
        i += 1

    if not os.path.exists(out_dir):
        print("Creating folder %s" % out_dir)
        os.mkdir(out_dir)

    while j < number_of_files:
        offset = offsets_array[j]
        (img_width, img_height) = struct.unpack_from('<LL', data, offset)
        offset += 8
        if (j != number_of_files - 1):
            zlibdata = data[offset:offsets_array[j + 1]]
        else:
            zlibdata = data[offset:filesize]
        zlib_decompress = zlib.decompress(zlibdata)
        im = Image.frombuffer('RGBA', (img_width, img_height), zlib_decompress, 'raw', 'RGBA', 0, 1)
        b,g,r,a = im.split()
        rgb = Image.merge("RGBA", (r,g,b,a))
        out_path = os.path.join(out_dir, 'img_' + str(j).zfill(2) + '.png')
        print("Saving %s Width/Height=%dx%d" %(out_path, img_width, img_height))
        rgb.save(out_path)
        j += 1

match len(sys.argv):
    case 3:
        extract(sys.argv[1], sys.argv[2])
    case 2:
        extract(sys.argv[1], '.\\' + os.path.splitext(sys.argv[1])[0])
    case 1:
        for filename in os.scandir('.\\'):
            if filename.is_file() and filename.name.endswith('.anim'):
                extract(filename.name, os.path.splitext(filename)[0])
    case _:
        print("Usage: extract-anim.py <filename> <outdir>")
        print("   or: extract-anim.py <filename>")
        print("   or: extract-anim.py")
        input("\nPress Enter to exit...")
        sys.exit(1)

print("Extracting done. Enjoy!")
input("\nPress Enter to exit...")
sys.exit(1)