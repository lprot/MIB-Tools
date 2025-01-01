import os, sys, stat, subprocess, shutil
from pathlib import Path

# Ensure the script is run with Python 3
if sys.version_info[0] < 3:
    input("You need to run this script with Python 3!\nPress Enter to exit...")
    sys.exit(1)

# Install configparser if not already installed
try:
    import configparser
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'configparser'], stdout=subprocess.DEVNULL)
    import configparser

def main():
    # Use default file name or override with command-line parameter
    default_file = "metainfo2.txt"
    input_file = sys.argv[1] if len(sys.argv) > 1 else default_file

    # Check if the input file exists
    if not Path(input_file).exists():
        input(f"\nERROR! Cannot find {input_file}. Press Enter to exit...")
        sys.exit(1)

    # Ask user for region conversion
    us = input("\nConvert US(NAR)/CN/JP/KR(RoW) to EU unit? Enter 'y' for yes, or just press Enter for no: ").strip().lower()
    is_conversion_needed = us in {"y", "yes"}

    # Read configuration from the input file
    print(f"Reading {input_file}...")
    config = configparser.ConfigParser()
    config.optionxform = str  # Preserve case sensitivity for options
    config.read(input_file)

    if len(config.sections()) == 0:
        input(f"\nERROR! Cannot read {input_file}. Press Enter to exit...")
        sys.exit(1)

    # Prepare a new configuration
    config2 = configparser.ConfigParser()
    config2.optionxform = str

    variant_map = {
        "17204": "17208",
        "17205": "17213",
        "17206": "17210",
        "17207": "17212",
        "17214": "17218",
        "17215": "17223",
        "17216": "17220",
        "17217": "17222",
        "17225": "17221",
        "17226": "17219",
    }

    new_id = ""
    user_id = ""
    for section in config.sections():
        if not config2.has_section(section):
            config2.add_section(section)

            for option, value in config.items(section):
                if option == "RequiredVersionOfDM":
                   config2.set(section, option, '"0"')
                elif is_conversion_needed and option.startswith("Region") and value == '"Europe"':
                   config2.set(section, "Region", '"Europe"')
                   config2.set(section, "Region2", '"RoW"')
                   config2.set(section, "Region3", '"USA"')
                   config2.set(section, "Region4", '"CN"')
                elif is_conversion_needed and option.startswith("Variant") and value.strip('"') in variant_map:
                     config2.set(section, option, f'"{variant_map[value.strip('\"')]}"')
                else:
                     config2.set(section, option, value)

                # Detect new ID for linking
                split_section = section.split("\\")
                if not new_id and len(split_section) == 5 and split_section[0] == "cpu" and split_section[1] == "customerupdateinfos":
                   new_id = split_section[2]
                   print(f"Found ID: {new_id}")
                   user_id = input("Enter SWDL HwVersion of your unit (see it in GEM>mibstd2_toolbox>mib_info): ").strip()
                   print(f"Linking ID: {user_id} to ID: {new_id}")

            if user_id and new_id and f"\\{new_id}\\" in section:
               new_section = section.replace(f"\\{new_id}\\", f"\\{user_id}\\")
               if not config2.has_section(new_section):
                  config2.add_section(new_section)
                  config2.set(new_section, "Link", f'"[{section}]"')

    if is_conversion_needed:
        print("\nIMPORTANT! This metainfo2.txt can only be used for converting US(NAR)/CN/JP/KR(RoW) units to EU units!")
        print("Before starting the update, patch `tsd.mibstd2.system.swdownload` using mibstd2_toolbox>Tools to accept any metainfo2.txt.")

    # Create a backup of the original file
    backup_file = Path(input_file).with_suffix(".bak")
    shutil.copy(input_file, backup_file)
    print(f"Backup created: {backup_file}")

    # Write updated configuration to the file
    with open(input_file, "w") as config_file:
        config2.write(config_file)

    os.chmod(input_file, stat.S_IWRITE | stat.S_IREAD | stat.S_IEXEC)

    input("\nDone. Press Enter to exit...")

if __name__ == "__main__":
    main()
