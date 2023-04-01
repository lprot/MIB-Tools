import os, sys

def convert(filename, out_dir):
    print('Processing: ' + os.path.splitext(filename)[0] + '.txt')
    txtFile = open(os.path.splitext(filename)[0] + '.txt', 'r')
    Lines = txtFile.readlines()
    print('Writing to: ' + os.path.splitext(filename)[0] + '.bin')
    binFile = open(os.path.splitext(filename)[0] + '.bin', 'wb')
    for line in Lines:
        if line.find('0x') > -1:
            binFile.write(bytearray.fromhex(line.strip().split('\t')[1].replace(' ','')))
    binFile.close()
    txtFile.close()
    print('Done.');

match len(sys.argv):
    case 2:
        convert(sys.argv[1], '.\\' + os.path.splitext(sys.argv[1])[0])
    case 1:
        for filename in os.scandir('.\\'):
            if filename.is_file() and filename.name.endswith('.txt'):
                convert(filename.name, os.path.splitext(filename)[0])
    case _:
        print("Usage: eeprom2bin.py <filename>")
        print("   or: eeprom2bin.py")
        input("\nPress Enter to exit...")
        sys.exit(1)

input("\nPress Enter to exit...")
sys.exit(1)