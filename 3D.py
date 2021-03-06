from matplotlib import pyplot as plt
from matplotlib.pyplot import MultipleLocator
import matplotlib.ticker as ticker
from matplotlib import animation
import numpy as np
import math
import threading
from SpringSimulator.Simulator import Spring
from SpringSimulator.Simulator import Particle
from SpringSimulator.Simulator import coordinate

f = 0.8  # friction coefficient
g = -9.81  # gravity
dt = 0.05  # differential time
stop_time = 30  # tot running time
time = 0  # time mark
t = np.arange(0, stop_time, dt)


def ad_force(var, fun, a1, a2, a3):
    force = a1 * fun(a2 * var) + a3
    return force


def initpos(x, y, l, theta):
    l = math.sqrt(3) / 3 * l

    x1 = x - l * math.sin(theta + 1 / 3 * math.pi)
    y1 = y - l * math.cos(theta + 1 / 3 * math.pi)

    x2 = x + l * math.sin(theta)
    y2 = y + l * math.cos(theta)

    x3 = x + l * math.cos(theta + 1 / 6 * math.pi)
    y3 = y - l * math.sin(theta + 1 / 6 * math.pi)

    return x1, y1, x2, y2, x3, y3


mass = np.arange(1, 3, 0.2)
mass = np.around(mass, decimals=2)

spring_coefficient = np.arange(1, 5, 0.5)  # spring_coefficient
spring_coefficient = np.around(spring_coefficient, decimals=1)

damping_coefficient = np.arange(0.1, 1, 0.1)  # damping_coefficient
damping_coefficient = np.around(damping_coefficient, decimals=1)

hight = np.arange(50, 80, 5)
hight = np.around(hight, decimals=2)


angle = np.arange(-math.pi / 3, 5*math.pi / 3, math.pi / 6)
angle = np.around(angle, decimals=3)

length = np.arange(10, 40, 5)
length = np.around(length, decimals=3)

a1R = np.arange(1, 30, 3)
a1R = np.around(a1R, decimals=3)

a2R = np.arange(1, 30, 3)
a2R = np.around(a2R, decimals=3)

a3R = np.arange(1, 30, 3)
a3R = np.around(a3R, decimals=3)


mass_plot_x = []
mass_plot_y = []
k_plot_x = []
k_plot_y = []
b_plot_x = []
b_plot_y = []
t_plot_x = []
t_plot_y = []


mass_plot = []
k_plot = []
b_plot = []

centre_of_mass = []
V_ms = []
x1y1_mv = []
av_x = []
for m in mass:
    for sc_v in spring_coefficient:
        for dc_v in damping_coefficient:
            # m = 1
            # dc_v = 0.8
            # sc_v = 2.8
            an = -math.pi / 3
            le = 40
            h = 50
            a1 = 20
            a2 = 1
            a3 = 0

            POS = initpos(0, h, le, an)  # x, y, edge_length, rot angle(rad)
            P1 = Particle(POS[0], POS[1], m)  # X, Y, mass
            P2 = Particle(POS[2], POS[3], m)
            P3 = Particle(POS[4], POS[5], m)

            S12 = Spring(sc_v, dc_v, P1, P2)  # spring_coefficient, damping_coefficient, particle_1, particle_2
            S23 = Spring(sc_v, dc_v, P2, P3)
            S13 = Spring(sc_v, dc_v, P1, P3)

            for i in t:
                if i == 0:
                    x1y1_mv.clear()
                S12.input_force = ad_force(i, math.sin, a1, a2, a3)
                coordinate(S12, S13, P1)
                coordinate(S12, S23, P2)
                coordinate(S13, S23, P3)
                B = 1/3 * (P1.x + P2.x + P3.x)
                centre_of_mass.append(B)
            av_x.append((centre_of_mass[-1] - centre_of_mass[0])/stop_time)
            mass_plot.append(m)
            k_plot.append(sc_v)
            b_plot.append(dc_v)
    # print("Progress: %s" % m)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

X, Y, Z = np.array(mass_plot), np.array(k_plot), np.array(b_plot)
AV = np.array(av_x)

cm = plt.cm.get_cmap('jet')
fig = ax.scatter3D(X, Y, Z, c=AV, cmap=cm)

cb = plt.colorbar(fig)
ax.set_xlabel('mass (kg)')
ax.set_ylabel('k (N/mm)')
ax.set_zlabel('b N/(mm/s)')
cb.ax.tick_params(labelsize=12)
cb.set_label('Average velocity along X-axis (mm/s)', size=14)

plt.show()



















