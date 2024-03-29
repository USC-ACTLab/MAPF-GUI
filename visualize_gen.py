#!/usr/bin/env python3
### This is the map/plan viewer for the MAPF instance generator project
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
    def __init__(self, config, schedule, map):
        self.config = config
        self.map = map
        self.schedule = schedule

        aspect = map["dimensions"][0] / map["dimensions"][1]

        self.fig = plt.figure(frameon=False, figsize=(4 * aspect, 4))
        self.ax = self.fig.add_subplot(111, aspect='equal')
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=None, hspace=None)
        # self.ax.set_frame_on(False)

        self.patches = []
        self.artists = []
        self.agents = dict()
        self.agent_names = dict()
        self.lines_x = []
        self.lines_y = []
        self.line_color = []
        # create boundary patch
        xmin = -0.5
        ymin = -0.5
        xmax = map["dimensions"][0] - 0.5
        ymax = map["dimensions"][1] - 0.5

        n_agents = len(config["agents"])

        # self.ax.relim()
        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)
        minor_ticks_x = np.arange(xmin, xmax, 1)
        minor_ticks_y = np.arange(ymin, ymax, 1)
        self.ax.set_xticks(minor_ticks_x, minor=True)
        self.ax.set_yticks(minor_ticks_y, minor=True)
        plt.grid(which='minor', axis='both', linewidth=2)
        # self.ax.set_xticks([])
        # self.ax.set_yticks([])
        # plt.axis('off')
        # self.ax.axis('tight')
        # self.ax.axis('off')

        self.patches.append(Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, facecolor='none', edgecolor='red'))
        for o in map["obstacles"]:
            x, y = o[0], o[1]
            self.patches.append(Rectangle((x - .5, y - 0.5), 1, 1, facecolor='red', edgecolor='red'))

        # create agents:
        self.T = 0
        # draw goals first
        for d, i in zip(config["agents"], range(0, len(config["agents"]))):
            name = d["name"]
            if "goal" in d:
                goals = [d["goal"]]
            if "potentialGoals" in d:
                goals = [goal for goal in d["potentialGoals"]]
            for goal in goals:
                self.patches.append(
                    Rectangle((goal[0] - 0.25, goal[1] - 0.25), 0.5, 0.5, facecolor=Colors[i % len(Colors)],
                              edgecolor='black', alpha=0.5))
                self.agent_names[name] = self.ax.text(d["goal"][0], d["goal"][1], name.replace('agent', ''))
                self.agent_names[name].set_horizontalalignment('center')
                self.agent_names[name].set_verticalalignment('center')
                self.artists.append(self.agent_names[name])

        for d, i in zip(config["agents"], range(0, len(config["agents"]))):
            name = d["name"]
            self.agents[name] = Circle((d["start"][0], d["start"][1]), 0.3, facecolor=Colors[i % len(Colors)],
                                       edgecolor=Colors_bright[i % len(Colors)], linewidth=4)
            self.agents[name].original_face_color = Colors[i % len(Colors)]
            self.line_color.append(Colors[i % len(Colors)])
            self.patches.append(self.agents[name])
            self.T = max(self.T, schedule["schedule"][name][-1]["t"])
            self.agent_names[name] = self.ax.text(d["start"][0], d["start"][1], name.replace('agent', ''))
            self.agent_names[name].set_horizontalalignment('center')
            self.agent_names[name].set_verticalalignment('center')
            self.artists.append(self.agent_names[name])
            xs = []
            ys = []
            sch = schedule["schedule"][name]

            for j in range(0, len(sch)):
                xs.append(sch[j]["x"])
                ys.append(sch[j]["y"])

            self.lines_x.append(xs)
            self.lines_y.append(ys)

        # self.ax.set_axis_off()
        # self.fig.axes[0].set_visible(False)
        # self.fig.axes.get_yaxis().set_visible(False)

        # self.fig.tight_layout()
        self.anim = animation.FuncAnimation(self.fig, self.animate_func,
                                            init_func=self.init_func,
                                            frames=int(self.T + 1) * 10,
                                            interval=100,
                                            blit=True)


    def save(self, file_name, speed):
        self.anim.save(
            file_name,
            "ffmpeg",
            fps=10 * speed,
            dpi=200),
        # savefig_kwargs={"pad_inches": 0, "bbox_inches": "tight"})

    def show(self):
        plt.show()

    def init_func(self):
        for p in self.patches:
            self.ax.add_patch(p)
        for a in self.artists:
            self.ax.add_artist(a)

        for i in range(0, len(self.line_color)):
            plt.plot(self.lines_x[i], self.lines_y[i], color=self.line_color[i], linewidth=2)
        return self.patches + self.artists

    def animate_func(self, i):
        for agent_name in self.schedule["schedule"]:
            agent = schedule["schedule"][agent_name]
            pos = self.getState(i / 10, agent)
            # pos = self.getState(i, agent)
            p = (pos[0], pos[1])
            # self.agents[agent_name].center = p
            if isinstance(self.agents[agent_name], Circle):
                self.agents[agent_name].center = p
            else:
                self.agents[agent_name].set_xy((p[0]-.25, p[1]-.25))
            self.agent_names[agent_name].set_position(p)

        # reset all colors
        for _, agent in self.agents.items():
            agent.set_facecolor(agent.original_face_color)

        # check drive-drive collisions
        # agents_array = [agent for _, agent in self.agents.items()]
        # for i in range(0, len(agents_array)):
        #     for j in range(i + 1, len(agents_array)):
        #         d1 = agents_array[i]
        #         d2 = agents_array[j]
        #         pos1 = np.array(d1.center)
        #         pos2 = np.array(d2.center)
        #         if np.linalg.norm(pos1 - pos2) < 0.7:
        #             d1.set_facecolor('red')
        #             d2.set_facecolor('red')
        #             print("COLLISION! (agent-agent) ({}, {})".format(i, j))

        return self.patches + self.artists

    def getState(self, t, d):
        idx = 0
        while idx < len(d) and d[idx]["t"] < t:
            idx += 1
        if idx == 0:
            return np.array([float(d[0]["x"]), float(d[0]["y"])])
        elif idx < len(d):
            posLast = np.array([float(d[idx - 1]["x"]), float(d[idx - 1]["y"])])
            posNext = np.array([float(d[idx]["x"]), float(d[idx]["y"])])
        else:
            return np.array([float(d[-1]["x"]), float(d[-1]["y"])])
        dt = d[idx]["t"] - d[idx - 1]["t"]
        t = (t - d[idx - 1]["t"]) / dt
        pos = (posNext - posLast) * t + posLast
        return pos


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="configuration for agents")
    parser.add_argument("schedule", help="schedule for agents")
    parser.add_argument('--video', dest='video', default=None,
                        help="output video file (or leave empty to show on screen)")
    parser.add_argument("--speed", type=int, default=1, help="speedup-factor")
    args = parser.parse_args()

    with open(args.config) as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)

    with open(args.schedule) as states_file:
        schedule = yaml.load(states_file, Loader=yaml.FullLoader)

    with open(config["map_path"]) as map_file:
        map_config = yaml.load(map_file, Loader=yaml.FullLoader)

    cost = 0
    for i in range(0, len(schedule["schedule"])):
        cost += schedule["schedule"]["agent" + str(i)][-1]["t"]
    print(f"Total cost is: {cost}")
    animation = Animation(config, schedule, map_config)

    if args.video:
        animation.save(args.video, args.speed)
    else:
        animation.show()
