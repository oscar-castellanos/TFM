#!/usr/bin/env python
import sys
import io
import yaml

# usage example: load_inventory_from_conf.py /etc/ansible/hosts config/config.yml

inventory_file = sys.argv[1]

with open(sys.argv[2], "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

number_of_hosts = config['number_of_client_nodes']
number_of_containers_per_node = config['number_of_containers_per_node']

structures = {}

for i in range(0,number_of_hosts,1):
    host_containers = []

    host_name = 'host' + str(i)

    for j in range(0,number_of_containers_per_node,1):
        cont_name = 'cont' + str(j)
        host_containers.append(host_name + "-" + cont_name)

    structures[host_name] = host_containers

print(structures)

## delete all previous host lines
with open(inventory_file, 'r') as file:
    # read a list of lines into data
    data = file.readlines()

# write lines until "[nodes]" line (included)
with open(inventory_file, "w") as file:
    i = 0

    while (i < len(data) and data[i] != "[nodes]\n"):
        file.write(data[i])
        i+= 1
    if (i < len(data)):
        file.write(data[i])

## write new info
for host in structures:

    container_list = structures[host]

    i = 0
    containers_formatted = "\'["

    while (i < len(container_list) - 1):
        containers_formatted += "\"" + container_list[i] + "\","
        i += 1
        
    containers_formatted += "\"" + container_list[i] + "\"]\'"

    # read lines
    with open(inventory_file, 'r') as file:
        # read a list of lines into data
        data = file.readlines()


    i = 0

    # skip to nodes
    while (i < len(data) and data[i] != "[nodes]\n"):
        i+=1

    i+=1

    # skip to desired node
    while (i < len(data) and host not in data[i]):
        i+=1

    host_info = host + " containers=" + containers_formatted + "\n"

    if (i < len(data)):
        data[i] = host_info
        with open(inventory_file, 'w') as file:
            file.writelines( data )
    else:
        new_line = host_info
        with open(inventory_file, 'a') as file:
            file.writelines( host_info )
