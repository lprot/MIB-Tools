#as per https://www.drive2.com/l/605899902332985777/
import argparse, sys
try:
    import crcmod
except ImportError:
    print("  crcmod module is missing!\n"
          "  install it by running:\n"
          "  pip3 install crcmod")
    input("\nPress Enter to exit...")
    sys.exit(1)
parser = argparse.ArgumentParser()
parser.add_argument("filename")
data = open(parser.parse_args().filename, 'rb').read()
crc32_adlatus32 = crcmod.mkCrcFun(0x104c11db7, initCrc=0, xorOut=0, rev=True)
print("CRC32_ADLATUS: %08X" %(crc32_adlatus32(data)))
