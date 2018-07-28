import json
import glob


def get_configs():
    configs_flat = [load_file(config) for config in glob.glob("../configs/*.json")]
    configs = {}
    for config in configs_flat:
        configs[config['thread_id']] = config
    return configs


def load_file(path):
    with open(path) as f:
        data = json.load(f)
    return data
