#!/usr/bin/env python3
import random

import yaml
import matplotlib
# matplotlib.use("Agg")
from matplotlib.patches import Circle, Rectangle, Arrow
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
import matplotlib.animation as animation
import argparse
import math

# Colors = ['orange']  # , 'blue', 'green']
# Colors = []
# for i in range(10):
#     Colors.append((random.random(), random.random(), random.random()))

cmap = plt.get_cmap("tab20")
Colors = cmap.colors

Colors_bright = [[x*0.8 for x in y] for y in Colors]

class Animation:
    def __init__(self, map):
        self.map = map

        aspect = map["map"]["dimensions"][0] / map["map"]["dimensions"][1]

        self.fig = plt.figure(frameon=False, figsize=(4 * aspect, 4))
        self.ax = self.fig.add_subplot(111, aspect='equal')
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=None, hspace=None)
        # self.ax.set_frame_on(False)

        self.patches = []
        self.artists = []
        self.agents = dict()
        self.agent_names = dict()
        # create boundary patch
        xmin = -0.5
        ymin = -0.5
        xmax = map["map"]["dimensions"][0] - 0.5
        ymax = map["map"]["dimensions"][1] - 0.5

        mobstacle_exist = True

        try:
            n_mobstacles = len(map["map"]["mobstacles"])
        except:
            # print("There are not mobile obstacles")
            mobstacle_exist = False
        n_agents = len(map["agents"])

        # self.ax.relim()
        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)
        # self.ax.set_xticks([])
        # self.ax.set_yticks([])
        # plt.axis('off')
        # self.ax.axis('tight')
        # self.ax.axis('off')

        self.patches.append(Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, facecolor='none', edgecolor='red'))
        for o in map["map"]["obstacles"]:
            x, y = o[0], o[1]
            self.patches.append(Rectangle((x - .5, y - .5), 1, 1, facecolor='red', edgecolor='red'))

        # create agents:
        self.T = 0
        # draw goals first
        for d, i in zip(map["agents"], range(0, len(map["agents"]))):
            if "goal" in d:
                goals = [d["goal"]]
            if "potentialGoals" in d:
                goals = [goal for goal in d["potentialGoals"]]
            name = d["name"]
            for goal in goals:
                self.patches.append(
                    Rectangle((goal[0] - 0.25, goal[1] - 0.25), .5, .5, facecolor=Colors[i % len(Colors)],
                              edgecolor='black', alpha=0.5))
                self.agent_names[name] = self.ax.text(d["goal"][0], d["goal"][1], name.replace('agent', ''))
                self.agent_names[name].set_horizontalalignment('center')
                self.agent_names[name].set_verticalalignment('center')
                self.artists.append(self.agent_names[name])


        for d, i in zip(map["agents"], range(0, len(map["agents"]))):
            name = d["name"]
            self.agents[name] = Circle((d["start"][0], d["start"][1]), 0.3, facecolor=Colors[i % len(Colors)],
                                       edgecolor=Colors_bright[i % len(Colors)], linewidth=4)
            self.agents[name].original_face_color = Colors[i % len(Colors)]
            self.patches.append(self.agents[name])
            self.agent_names[name] = self.ax.text(d["start"][0], d["start"][1], name.replace('agent', ''))
            self.agent_names[name].set_horizontalalignment('center')
            self.agent_names[name].set_verticalalignment('center')
            self.artists.append(self.agent_names[name])

        if mobstacle_exist:
            for d, i in zip(map["map"]["mobstacles"], range(0, n_mobstacles)):
                name = "agent" + str(n_agents + i)
                self.agents[name] = Rectangle((d[0] - .25, d[1] - .25), .5, .5, facecolor='gray', edgecolor='gray')
                self.agents[name].original_face_color = "gray"
                self.patches.append(self.agents[name])
                # self.T = max(self.T, schedule["schedule"][name][-1]["t"])
                self.agent_names[name] = self.ax.text(d[0], d[1], name.replace('agent', ''))
                self.agent_names[name].set_horizontalalignment('center')
                self.agent_names[name].set_verticalalignment('center')
                self.artists.append(self.agent_names[name])

        # for d, i in zip(map["map"]["mobstacles"], range(0, n_mobstacles)):
        #     name = "agent" + str(n_agents + i)
        #     self.agents[name] = Rectangle((d[0] - .25, d[1] - .25), .5, .5, facecolor='blue', edgecolor='gray')
        #     self.agents[name].original_face_color = "gray"
        #     self.patches.append(self.agents[name])
        #     self.agent_names[name] = self.ax.text(d[0], d[1], name.replace('agent', ''))
        #     self.agent_names[name].set_horizontalalignment('center')
        #     self.agent_names[name].set_verticalalignment('center')
        #     self.artists.append(self.agent_names[name])


    def show(self):
        plt.show()

    def init_func(self):
        for p in self.patches:
            self.ax.add_patch(p)
        for a in self.artists:
            self.ax.add_artist(a)
        return self.patches + self.artists


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("map", help="input file containing map")
    parser.add_argument("--legacy", type=int, default=1, help="new map or legacy format (defult is legacy(1), 0 for new format)")
    parser.add_argument('--video', dest='video', default=None,
                        help="output video file (or leave empty to show on screen)")
    parser.add_argument("--speed", type=int, default=1, help="speedup-factor")
    args = parser.parse_args()

    with open(args.map) as map_file:
        map = yaml.load(map_file, Loader=yaml.FullLoader)

    if not args.legacy:
        # Using new map format. The map is in map["map_path"]
        map_path = map["map_path"]
        with open(map_path) as map_path:
            actual_map = yaml.load(map_path, Loader=yaml.FullLoader)

        # create new dict file to match the old map format
        new_map = {"map": actual_map, "agents": map["agents"]}
        map = new_map

    animation = Animation(map)

    animation.init_func()
    animation.show()

