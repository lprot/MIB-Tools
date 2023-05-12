import os, sys

def convert(filename):
    print('Processing: ' + filename)
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
        convert('.\\' + os.path.splitext(sys.argv[1])[0])
    case 1:
        for root, dirs, files in os.walk("."):
            path = root.split(os.sep)
            for file in files:
                if (root+file).endswith('.txt'):
                        convert(root+'\\'+file)
    case _:
        print("Usage: eeprom2bin.py <filename>")
        print("   or: eeprom2bin.py")
        input("\nPress Enter to exit...")
        sys.exit(1)

input("\nPress Enter to exit...")
sys.exit(1)