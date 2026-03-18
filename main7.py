import random
import math
import matplotlib
import numpy as np
from matplotlib import pyplot as plt


class source:  # класс источника
    def __init__(self, x0, y0, z0):
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0


def ray():  # функция задающая произвольные параметры l,n,m для прямой
    while True:
        l = random.uniform(-1, 1)
        n = random.uniform(-1, 1)
        m = random.uniform(-1, 1)
        length = (l ** 2 + n ** 2 + m ** 2) ** 0.5
        if length < 1:
            break
    l = l / length
    n = n / length
    m = m / length
    return l, n, m


class cl_direct():  # класс ребер куба
    def __init__(self, P1, P2, plane1, plane2):
        self.P1 = P1
        self.P2 = P2
        self.A = plane1.A - plane2.A
        self.B = plane1.B - plane2.B
        self.C = plane1.C - plane2.C
        self.D = plane1.D - plane2.D


class cl_plane():  # класс плоскостей
    def __init__(self, P1, P2, P3, P4):
        self.A = P1[1]*P2[2] + P2[1]*P3[2] + P3[1]*P1[2] - P3[1]*P2[2] - P1[1]*P3[2] - P2[1]*P1[2]
        self.B = P1[2]*P2[0] + P2[2]*P3[0] + P3[2]*P1[0] - P3[2]*P2[0] - P1[2]*P3[0] - P2[2]*P1[0]
        self.C = P1[0]*P2[1] + P2[0]*P3[1] + P3[0]*P1[1] - P3[0]*P2[1] - P1[0]*P3[1] - P2[0]*P1[1]
        self.D = -(P1[2]*P2[0]*P3[1] + P1[1]*P2[2]*P3[0] + P1[0]*P2[1]*P3[2]
                   - P1[1]*P2[0]*P3[2] - P1[2]*P2[1]*P3[0] - P1[0]*P2[2]*P3[1])
        self.p1 = P1
        self.p2 = P2
        self.p3 = P3
        self.p4 = P4

    def pl_dir(self, dt1, dt2, dt3, dt4):
        self.direct = [dt1, dt2, dt3, dt4]


def inside(x, y, z, plane):
    deltax = (plane.direct[0].P1[0] + plane.direct[0].P2[0]) / 2 - x
    deltay = (plane.direct[0].P1[1] + plane.direct[0].P2[1]) / 2 - y
    deltaz = (plane.direct[0].P1[2] + plane.direct[0].P2[2]) / 2 - z
    length = (deltax**2 + deltay**2 + deltaz**2) ** 0.5

    l = deltax / length
    n = deltay / length
    m = deltaz / length

    count_dr = 0

    for i in range(4):
        znamen = plane.direct[i].A*l + plane.direct[i].B*n + plane.direct[i].C*m
        if znamen != 0:
            t = -(plane.direct[i].A*x + plane.direct[i].B*y +
                  plane.direct[i].C*z + plane.direct[i].D) / znamen

            x0 = t*l + x
            y0 = t*n + y
            z0 = t*m + z

            len1 = ((plane.direct[i].P1[0] - plane.direct[i].P2[0])**2 +
                    (plane.direct[i].P1[1] - plane.direct[i].P2[1])**2 +
                    (plane.direct[i].P1[2] - plane.direct[i].P2[2])**2)

            len2 = ((plane.direct[i].P1[0] - x0)**2 +
                    (plane.direct[i].P1[1] - y0)**2 +
                    (plane.direct[i].P1[2] - z0)**2)

            len3 = ((x0 - plane.direct[i].P2[0])**2 +
                    (y0 - plane.direct[i].P2[1])**2 +
                    (z0 - plane.direct[i].P2[2])**2)

            if (t >= 0.0) and (len1 > len2 + len3):
                count_dr += 1

    if count_dr % 2 != 0:
        return 1
    else:
        return 0


def kub(s):
    eps = 1e-9
    for i in range(6):
        val = plane[i].A * s.x0 + plane[i].B * s.y0 + plane[i].C * s.z0 + plane[i].D
        if abs(val) < eps:
            return 1.0
    count = 0
    N = 1000

    for j in range(N):
        l, n, m = ray()
        count_pl = 0

        for i in range(6):
            znamen = (plane[i].A*l + plane[i].B*n + plane[i].C*m)

            if znamen != 0:
                t = -(plane[i].A*s.x0 + plane[i].B*s.y0 +
                      plane[i].C*s.z0 + plane[i].D) / znamen

                if t >= 0:
                    x = s.x0 + l*t
                    y = s.y0 + n*t
                    z = s.z0 + m*t

                    count_pl += inside(x, y, z, plane[i])

        if count_pl >= 1:
            count += 1

    return count / N


print("введите длину ребра куба")
d = int(input())
print("сколько источников?")
n_sources = int(input())
sources = []
for i in range(n_sources):
    print(f"введите x y z для источника {i+1}")
    x0 = float(input())
    y0 = float(input())
    z0 = float(input())
    sources.append(source(x0, y0, z0))
P = [
    [-d/2, -d/2, d/2],
    [-d/2, d/2, d/2],
    [d/2, d/2, d/2],
    [d/2, -d/2, d/2],
    [-d/2, -d/2, -d/2],
    [-d/2, d/2, -d/2],
    [d/2, d/2, -d/2],
    [d/2, -d/2, -d/2]
]

plane = []

plane.append(cl_plane(P[0], P[1], P[2], P[3]))
plane.append(cl_plane(P[1], P[2], P[6], P[5]))
plane.append(cl_plane(P[4], P[5], P[6], P[7]))
plane.append(cl_plane(P[0], P[3], P[7], P[4]))
plane.append(cl_plane(P[2], P[3], P[7], P[6]))
plane.append(cl_plane(P[0], P[1], P[5], P[4]))

direct = []

direct.append(cl_direct(P[0], P[1], plane[0], plane[5]))
direct.append(cl_direct(P[0], P[3], plane[0], plane[3]))
direct.append(cl_direct(P[0], P[4], plane[3], plane[5]))
direct.append(cl_direct(P[2], P[1], plane[0], plane[1]))
direct.append(cl_direct(P[2], P[3], plane[0], plane[4]))
direct.append(cl_direct(P[2], P[6], plane[1], plane[4]))
direct.append(cl_direct(P[5], P[1], plane[1], plane[5]))
direct.append(cl_direct(P[5], P[4], plane[2], plane[5]))
direct.append(cl_direct(P[5], P[6], plane[1], plane[2]))
direct.append(cl_direct(P[7], P[3], plane[3], plane[4]))
direct.append(cl_direct(P[7], P[4], plane[2], plane[3]))
direct.append(cl_direct(P[7], P[6], plane[2], plane[4]))

plane[0].pl_dir(direct[0], direct[1], direct[3], direct[4])
plane[1].pl_dir(direct[3], direct[5], direct[6], direct[8])
plane[2].pl_dir(direct[7], direct[8], direct[10], direct[11])
plane[3].pl_dir(direct[1], direct[2], direct[9], direct[10])
plane[4].pl_dir(direct[4], direct[5], direct[9], direct[11])
plane[5].pl_dir(direct[0], direct[2], direct[6], direct[7])

probs = []
r_vals = []

for s in sources:
    p = kub(s)
    probs.append(p)
    r = (s.x0**2 + s.y0**2 + s.z0**2) ** 0.5
    r_vals.append(r)
plt.scatter(r_vals, probs, label="численно")
plt.xlabel("r")
plt.ylabel("P")
zed = np.linspace(0, 3*d, 1000)
P = np.zeros_like(zed)
for i, zi in enumerate(zed):
    if abs(zi) <= d/2:
        P[i] = 1
    else:
        r = abs(zi)
        P[i] = 0.5 * (d/2)**2 / r**2

plt.plot(zed, P, label="теоретическая")
plt.grid(True)
plt.legend()
plt.show()

s = source(d/2, d/2, d/2)
print("источник в вершине:", kub(s))

s = source(0, 0, 0)
print("источник в центре:", kub(s))

s = source(0, 0, d/2)
print("источник в центре грани:", kub(s))

s = source(d/2, 0, d/2)
print("источник в центре ребра:", kub(s))