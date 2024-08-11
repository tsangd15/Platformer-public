"""Config Handler Module"""
import json


default_config = {"music": True,
                  "sound_effects": True}


def validate_config(config):
    """Validate the values in given config dict"""
    # boolean keys
    keys_bool = ("music", "sound_effects")

    for key in keys_bool:
        # check if key not in config or not bool type
        if (key not in config) or not isinstance(config[key], bool):
            return False

    return True


def load_config():
    """Load the saved settings from config.json"""
    with open("config.json", "r") as file:
        contents = file.read()

    config = json.loads(contents)

    if validate_config(config):
        return config

    # otherwise invalid, run code below
    print("Invalid config detected. Returned default.")
    return default_config


def save_config(new_config):
    """Save the current settings to config.json"""
    if validate_config(new_config):
        save = new_config
    else:
        print("Invalid config detected. Replaced with default.")
        save = default_config

    with open("config.json", "w") as file:
        file.write(json.dumps(save, indent=4, sort_keys=True) + "\n")
