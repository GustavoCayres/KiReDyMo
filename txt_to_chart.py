import sys
import numpy as np
import matplotlib.pyplot as plt


with open(sys.argv[1]) as data_file:
    v = np.loadtxt(data_file, delimiter="\t", dtype='int', skiprows=1, usecols=(0,))

v_hist = np.ravel(v)   # 'flatten' v
fig = plt.figure()
ax1 = fig.add_subplot(111)

n, bins, patches = ax1.hist(v_hist, bins=50, normed=1, facecolor='green')
plt.show()
