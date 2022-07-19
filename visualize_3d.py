# Visualize solved MAPF instance in 3D
import argparse

import numpy as np
import matplotlib.pyplot as plt
import yaml
from mpl_toolkits.mplot3d import Axes3D
import argparse


def drawObs(data, obs):
    for ob in obs:
        data[ob[0], ob[1], :] = 1

def drawPath(path):
    makespan = path[-1]['t']
    x, y = [], []
    for p in path:
        x.append(int(p['x']))
        y.append(int(p['y']))
    z = range(int(makespan+1))
    return x, y, z


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("map", help='map yaml file')
    parser.add_argument("path", help='solved MAPF instance yaml file')
    args = parser.parse_args()

    with open(args.map) as map_file:
        map_data = yaml.load(map_file, Loader=yaml.FullLoader)

    with open(args.path) as path_file:
        path_data = yaml.load(path_file, Loader=yaml.FullLoader)

    dim = map_data["dimensions"]
    obs = map_data["obstacles"]
    agents = path_data["schedule"]

    makespan = 0
    for agent in agents:
        if makespan < agents[agent][-1]['t']:
            makespan = agents[agent][-1]['t']

    data = np.zeros(shape=(dim[0], dim[1], makespan+1))
    drawObs(data, obs)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # ax.set_box_aspect((dim[0], dim[1], makespan+1))


    ax.voxels(data, alpha=.6)
    for agent in agents:
        x,y,z = drawPath(agents[agent])
        ax.plot3D(x,y,z)

    plt.show()