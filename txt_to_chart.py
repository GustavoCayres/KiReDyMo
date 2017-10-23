import sys
import numpy as np
import matplotlib.pyplot as plt


plt.plotfile(sys.argv[1], delimiter="\t", skiprows=0, cols=(0, 1))
plt.show()
