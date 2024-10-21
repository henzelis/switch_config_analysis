import os
import json
from ttp import ttp


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def convert(template_path: str, configuration_path: str, result_file: str):
    template_exist = os.path.exists(template_path)
    configuration_exists = os.path.exists(configuration_path)
    if template_exist and configuration_exists:
        with open(configuration_path) as file:
            configuration = file.read()
        with open(template_path) as file:
            template = file.read()
        parser = ttp(configuration, template)
        parser.parse()
        data_dict = parser.result()[0][0]
        json_data = json.dumps(data_dict, indent=4)
        with open(result_file, "w") as f:
            f.write(json_data)
        print(
            bcolors.OKGREEN
            + f"File {configuration_path.split('/')[-1]} converted to {result_file}"
            + bcolors.ENDC
        )


if __name__ == "__main__":
    configuration_path = "ftd_config.txt"
    template_path = "tp_link_switch_ttp.txt"
    convert(template_path, configuration_path)
