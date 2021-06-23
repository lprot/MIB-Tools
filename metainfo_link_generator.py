import sys
if sys.version_info[0] < 3:
    raw_input("You need to run this with Python 3!\nPress Enter to exit...")
    sys.exit(1)

import subprocess, pkg_resources
required = {'configparser'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

import configparser, os

if len(sys.argv) < 5:
    print("Usage: " + os.path.basename(__file__) + " <inputfile> <outputfile> <ID for change> <ID to change>")
    print("Example: " + os.path.basename(__file__) + " metainfo2.txt metainfo2.out 20 14")
    input("\nPress Enter to exit...")
    sys.exit(1) 

config = configparser.ConfigParser()
config.optionxform = str
config.read(sys.argv[1])

config2 = configparser.ConfigParser()
config2.optionxform = str

for section in config.sections():
    config2.add_section(section)
    for option in config.options(section):
        config2.set(section, option, config.get(section, option))
    if "\\" + sys.argv[3] + "\\" in section:
        newsection = section.replace("\\" + sys.argv[3] + "\\", "\\" + sys.argv[4] + "\\")
        if not config2.has_section(newsection):
            config2.add_section(newsection)
            config2.set(newsection, "Link", '"[' + section + ']"')

with open(sys.argv[2], "w") as config_file:
    config2.write(config_file)

input("\nDone. Press Enter to exit...")
