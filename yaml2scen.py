#!/usr/bin/env python3
import yaml
import argparse
import numpy as np

def scen_map_gen(map_config, scen_map_file):
    dim = map_config["dimensions"]
    obstacles = map_config["obstacles"]

    with open(scen_map_file, 'w') as f:
        f.write(f"type octile\n")
        f.write(f"height {int(dim[1])}\n")
        f.write(f"width {int(dim[0])}\n")
        f.write(f"map\n")

        map_mask = np.zeros((int(dim[1]), int(dim[0])), dtype=bool)
        if obstacles:
            for obs in obstacles:
                map_mask[int(obs[1]), int(obs[0])] = True

        for i in range(int(dim[1])):
            line = ""
            for j in range(int(dim[0])):
                if map_mask[i, j] == True:
                    line += '@'
                else:
                    line += '.'
            f.write(f"{line}\n")
    return int(dim[1]), int(dim[0])

def scen_gen(agent_config, scen_file, scen_map_file, height, width):
    with open(scen_file, 'w') as f:
        f.write(f"version 1\n")

        agents = agent_config["agents"]
        for i in range(len(agents)):
            f.write(f"1  {scen_map_file}  {width}  {height}  ")
            start = agents[i]["start"]
            goal = agents[i]["goal"]
            f.write(f"{start[0]}  {start[1]}  ")
            f.write(f"{goal[0]}  {goal[1]}  1.0\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("yaml", help="start/goal yaml file")
    parser.add_argument("output", help="output scen file name")

    args = parser.parse_args()

    # read yaml config
    yaml_file = args.yaml

    with open(yaml_file, 'r') as f:
        agent_config = yaml.load(f, Loader=yaml.FullLoader)
    f.close()

    map_file = agent_config["map_path"]

    with open(map_file, 'r') as f:
        map_config = yaml.load(f, Loader=yaml.FullLoader)

    scen_file = args.output
    scen_file_prefix = scen_file.split('.')[0]

    scen_file = scen_file_prefix + '.scen'
    scen_map_file = scen_file_prefix + '.map'


    height, width = scen_map_gen(map_config, scen_map_file)
    scen_gen(agent_config, scen_file, scen_map_file, height, width)

