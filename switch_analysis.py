from ttp_parser import bcolors, convert
from mydict import MyDict
import json
import re
import os
import glob

config_path_list = [r'D:\GoogleDrive\Мій диск\Alesta\NAZK\For_Alesta_LAN\79+',
                    r'D:\GoogleDrive\Мій диск\Alesta\NAZK\For_Alesta_LAN\303+',
                    r'D:\GoogleDrive\Мій диск\Alesta\NAZK\For_Alesta_LAN\610+',
                    r'D:\GoogleDrive\Мій диск\Alesta\NAZK\For_Alesta_LAN\708+',
                    r'D:\GoogleDrive\Мій диск\Alesta\NAZK\For_Alesta_LAN\Зал засідання+',
                    r'D:\GoogleDrive\Мій диск\Alesta\NAZK\For_Alesta_LAN\к.428',
                    r'D:\GoogleDrive\Мій диск\Alesta\NAZK\For_Alesta_LAN\Кінозал',
                    r'D:\GoogleDrive\Мій диск\Alesta\NAZK\For_Alesta_LAN']

for conf_dir in config_path_list:
    for file_path in glob.glob(os.path.join(conf_dir, '*.txt')):
        file_name = os.path.split(file_path)[-1]
        json_file_path = file_path.replace('.txt', '.json')
        # if "TL-33_11.33.txt" in file_name:
        #     print("here it is!")
        if "HP" in file_name:
            template_path = 'hp_switch_ttp.txt'
        elif "TL" in file_name:
            template_path = 'tp_link_switch_ttp.txt'
        convert(template_path, file_path, json_file_path)
        print(f"File created{json_file_path}")

access_vlans_dict = {}
for conf_dir in config_path_list:
    for file_path in glob.glob(os.path.join(conf_dir, '*.json')):
        file_name = os.path.split(file_path)[-1]
        hostname = file_name.split('.')[0]
        with open(file_path) as file:
            data = MyDict(json.loads(file.read()))
            access_vlans_list = []
            for interface in data.interfaces:
                access_vlan = data.interfaces[interface].get('access_vlan')
                print(access_vlan)
                if access_vlan is not None:
                    access_vlans_list.append(int(access_vlan))
            access_vlans_list = list(set(access_vlans_list))
            access_vlans_dict[hostname] = access_vlans_list
print(access_vlans_dict)




print("Converting switch configuration to JSON")
configuration_path = "core_tplink.txt"
template_path = "tp_link_switch_ttp.txt"
result_file = "tp-link.json"

convert(template_path, configuration_path, result_file)

with open(result_file) as file:
    data = MyDict(json.loads(file.read()))

core_vlan_list = []
for vlan in data.vlans:
    core_vlan_list.append(int(data.vlans[vlan]['vlan_num']))

print(core_vlan_list)

with open('ftd.json') as file:
    ftd_data = MyDict(json.loads(file.read()))

dhcp_vlan_name_list = []
for intf in ftd_data.dhcp:
    if intf is not None:
        dhcp_vlan_name_list.append(intf)

print(f"List of names DHCP enabled on FTD {dhcp_vlan_name_list}")
print(f"Count of DHCP enabled VLANS: {len(dhcp_vlan_name_list)}")

regex = r"(\d+)"
dhcp_vlan_ftd_list = []
for vlan_name in dhcp_vlan_name_list:
    result = re.search(regex, vlan_name)
    try:
        vlan_number = result.group(0)
    except Exception as error:
        # print(error)
        pass
    if result is not None:
        dhcp_vlan_ftd_list.append(int(vlan_number))

dhcp_vlan_ftd_list.sort()

print(f"DHCP enabled VLANS on FTD {dhcp_vlan_ftd_list}")
print(f"Count of DHCP enabled VLANS: {len(dhcp_vlan_ftd_list)}")

non_dhcp_vlan_list = []
for vlan in core_vlan_list:
    if vlan not in dhcp_vlan_ftd_list:
        non_dhcp_vlan_list.append(vlan)
print(
    f"Non DHCP VLANS on CORE switch: {non_dhcp_vlan_list} \n Number of not DHCP enabled VLANs: {len(non_dhcp_vlan_list)}")

non_core_dhcp_vlans = []
for vlan in dhcp_vlan_ftd_list:
    if vlan not in core_vlan_list:
        non_core_dhcp_vlans.append(vlan)
print(f"DHCP VLANs not present on CORE switch: {non_core_dhcp_vlans}")

all_vlans_ftd_list = []
for interface in ftd_data.interfaces:
    try:
        vlan = ftd_data.interfaces[interface]['vlan']
        all_vlans_ftd_list.append(int(vlan))
    except Exception as error:
        pass

print(f"All VLANs list on FTD: {all_vlans_ftd_list}, number of VLANs is: {len(all_vlans_ftd_list)}")

not_on_ftd_vlan_list = []
for vlan in core_vlan_list:
    if vlan not in all_vlans_ftd_list:
        not_on_ftd_vlan_list.append(vlan)

print(
    f"Not terminated on FTD VLANs present on CORE Switch: {not_on_ftd_vlan_list}, count: {len(not_on_ftd_vlan_list)} ")
