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

import configparser, os, stat

config = configparser.ConfigParser()
config.optionxform = str
us = input("Do you want to convert US(NAR)/CN/JP/KR(RoW) to EU unit? Enter y if yes, or just press enter if no: ")
print("Reading metainfo2.txt...")
config.read("metainfo2.txt")
if len(config) == 1:
    input("\nERROR! Cannot open metainfo2.txt. Press any key to exit...")
    exit()

config2 = configparser.ConfigParser()
config2.optionxform = str

new_id = ""

for section in config.sections():
    if not config2.has_section(section):
        config2.add_section(section)
        for option in config.options(section):
            if option == "RequiredVersionOfDM":
                config2.set(section, option, '"0"')
            elif us == "y" and option.startswith("Region") and config.get(section, option) == '"Europe"':
                config2.set(section, "Region", '"Europe"')
                config2.set(section, "Region2", '"RoW"')
                config2.set(section, "Region3", '"USA"')
                config2.set(section, "Region4", '"CN"')
            elif us == "y" and option.startswith("Variant") and config.get(section, option) == '"17214"':
                config2.set(section, option, '"17218"')
            elif us == "y" and option.startswith("Variant") and config.get(section, option) == '"17216"':
                config2.set(section, option, '"17220"')
            elif us == "y" and option.startswith("Variant") and config.get(section, option) == '"17226"':
                config2.set(section, option, '"17219"')
            elif us == "y" and option.startswith("Variant") and config.get(section, option) == '"17225"':
                config2.set(section, option, '"17221"')
            elif us == "y" and option.startswith("Variant") and config.get(section, option) == '"17217"':
                config2.set(section, option, '"17222"')
            elif us == "y" and option.startswith("Variant") and config.get(section, option) == '"17215"':
                config2.set(section, option, '"17223"')
            elif us == "y" and option.startswith("Variant") and config.get(section, option) == '"17206"':
                config2.set(section, option, '"17210"')
            elif us == "y" and option.startswith("Variant") and config.get(section, option) == '"17224"':
                config2.set(section, option, '"17212"')
            elif us == "y" and option.startswith("Variant") and config.get(section, option) == '"17205"':
                config2.set(section, option, '"17213"')
            else:
                config2.set(section, option, config.get(section, option))
            split_section = section.split("\\")
            if new_id == "" and len(split_section) == 5 and split_section[0] == 'cpu' and split_section[1] == 'customerupdateinfos':
                new_id = split_section[2]
                print("Found ID: " + str(new_id))
                id = input('Enter SWDL HwVersion of your unit (you can find it in mibstd2_toolbox>mib_info): ').strip()
                print("Linking ID: " + str(id) + " to ID: " + str(new_id))
        if id and new_id and "\\" + new_id + "\\" in section:
            newsection = section.replace("\\" + new_id + "\\", "\\" + id + "\\")
            if not config2.has_section(newsection):
                config2.add_section(newsection)
                config2.set(newsection, "Link", '"[' + section + ']"')

if us == "y":
    print("\nIMPORTANT! This metainfo2.txt can only be used on US(NAR)/CN/JP/KR(RoW) unit for convertion to EU unit!")
    print("Before starting the update, run mibstd2_toolbox>Tools>Patch tsd.mibstd2.system.swdownload to accept any metainfo2.txt!!!")

with open("metainfo2.old", "w") as config_file:
    config.write(config_file)

os.chmod("metainfo2.txt", stat.S_IWRITE)
with open("metainfo2.txt", "w") as config_file:
    config2.write(config_file)

input("\nDone. Press Enter to exit...")
