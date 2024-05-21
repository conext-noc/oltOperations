import os
import re

from helpers.constants.definitions import CONF_FILES, OnuInstall
from dataclasses import asdict


def parse_conf_file(*, file_path):
    commands = {"gpon": [], "bbs-config": []}
    current_section = None
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("#") or not line or line.startswith("<"):
                continue
            if line.startswith("[") and line.endswith("]"):
                current_section = line[1:-1]
            elif current_section:
                commands[current_section].append(line)
    return commands


def parse_gpon_config(*, config_file, **kwargs):
    commands = parse_conf_file(file_path=config_file)["gpon"]
    interpreted_commands = []
    for command in commands:
        interpreted_command = command.format(**kwargs)
        interpreted_commands.append(interpreted_command)
    return interpreted_commands


def parse_bbs_config(*, config_file, **kwargs):
    commands = parse_conf_file(file_path=config_file)["bbs-config"]
    interpreted_commands = []
    for command in commands:
        interpreted_command = command.format(**kwargs)
        interpreted_commands.append(interpreted_command)
    return interpreted_commands

# CONVERT INTO CLASS
def config_parser(*, device_like:str, data:OnuInstall, selection: int = None):
    print(selection)
    config_files = []
    config_file = ""
    selection = None
    selected = None

    for file in os.listdir(CONF_FILES):
        if file.endswith(".conf") and device_like in file:
            config_files.append(file[:-5])

    if len(config_files) == 0:
        print("There's No Such config file for desired ONT")

    if len(config_files) > 1 and selection is None:
        print(
            "There's More than 1 device matching the model, choose the desired device"
        )
        for idx, dev in enumerate(config_files):
            print(f" - [{idx}]  :  {dev}")
        selected = input("Select the index for the desired config   :   ").lower()
        selection = int(selected)
        config_file = CONF_FILES + "/" + config_files[int(selected)] + ".conf"

    if len(config_files) > 1 and selection is not None:
        config_file = CONF_FILES + "/" + config_files[selection] + ".conf"

    if len(config_files) == 1:
        config_file = CONF_FILES + "/" + config_files[0] + ".conf"

    onu_data = asdict(data)
    interpreted_gpon_commands = parse_gpon_config(
        config_file=config_file,
        **onu_data,
    )

    interpreted_bbs_config_commands = parse_bbs_config(
        config_file=config_file,
        **onu_data,
    )

    return {"gpon": interpreted_gpon_commands, "bbs": interpreted_bbs_config_commands, "selected": selection}
