"""Miscelaneous functions."""


import json
import os
import sys
from typing import Dict, List


def read_json_local(path: str):
    """Read JSON from local path."""
    with open(path, 'r') as f:
        file = json.load(f)
    return file


def load_configuration_file(optionsPath: str):
    """
    Checks if the file that's searched (specifically options in JSON)
    and reads the file to memory if found and content is correct.
    """
    if os.path.isfile(optionsPath):
        optionsFile = read_json_local(optionsPath)
        if len(optionsFile) == 0:
            print("*\nEmpty options file.")
            return False
        else:
            return optionsFile
    else:
        print("*\nMissing or wrongly named options file.")
        return False


def unpack_meta_scraper_config(config_options: Dict) -> List:
    """Unpack meta scraper configuration."""
    if config_options is False:
        print("\nMissing, empty or wrongly named config file. \
            Program will terminate.")
        sys.exit()
    else:
        print("\nFetching options from configuration file: ")
        print("# -------------------------------------- #")
        for option in config_options.keys():
            print(f"\t* {option}: {config_options[option]}")
        print()
        header = config_options["HEADER"]
        url = config_options["URL"]
        chrome_driver_path = config_options["CHROME_DRIVER_PATH"]
        output_path = config_options["OUTPUT_PATH"]

    return [header, url, chrome_driver_path, output_path]
