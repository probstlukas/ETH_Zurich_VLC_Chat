import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# Distance
X = np.array([2, 5, 10, 15, 20, 30, 40])
x_count = X.size
# Payload size
Y = np.array([1, 100, 200])
y_count = Y.size

throughputs = np.zeros(shape=(X.size, Y.size))
mean_delays = np.zeros(shape=(X.size, Y.size))
standard_deviation_delays = np.zeros(shape=(X.size, Y.size))
width_of_confidence_interval = np.zeros(shape=(X.size, Y.size))
success_rates_150B = np.zeros(X.size)
success_rates_35cm = np.zeros(Y.size)

for (i, x) in enumerate(X):
    for (j, y) in enumerate(Y):
        with open(f"results/{y}B-{x}cm.csv", "r") as f:
            #f.write(", ".join([str(i) for i in [standard_deviation, data_throughput, mean_packet_delay, success_rate, cl, cr]]))
            (standard_deviation, data_throughput, mean_packet_delay, success_rate, cl, cr) = list(map(float, f.readline().split(", ")))
            throughputs[i][j] = data_throughput
            mean_delays[i][j] = mean_packet_delay
            standard_deviation_delays[i][j] = standard_deviation
            width_of_confidence_interval[i][j] = cr - cl

X_m, Y_m = np.meshgrid(X, Y)

### Throughput
plt3D, ax = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax.plot_surface(X_m, Y_m, throughputs.transpose(), cmap=cm.coolwarm, linewidth=0, antialiased=True)
ax.set_xlabel("distance [cm]")
ax.set_ylabel("packet payload size [B]")
ax.set_zlabel("throughput [B/s]")
# Add a color bar which maps values to colors.
plt3D.colorbar(surf, shrink=0.5, aspect=5)
plt.show()

### Delay
plt3D, ax = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax.plot_surface(X_m, Y_m, mean_delays.transpose(), cmap=cm.coolwarm, linewidth=0, antialiased=True)
ax.set_xlabel("distance [cm]")
ax.set_ylabel("packet payload size [B]")
ax.set_zlabel("packet delay [s]")
# Add a color bar which maps values to colors.
plt3D.colorbar(surf, shrink=0.5, aspect=5)
plt.show()

### Standard deviation
plt3D, ax = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax.plot_surface(X_m, Y_m, standard_deviation_delays.transpose(), cmap=cm.coolwarm, linewidth=0, antialiased=True)
#ax.invert_xaxis()
ax.set_xlabel("distance [cm]")
ax.set_ylabel("payload size [B]")
ax.set_zlabel("standard deviation [s]")
# Add a color bar which maps values to colors.
plt3D.colorbar(surf, shrink=0.5, aspect=5)
plt.show()

### Confidence interval
plt3D, ax = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax.plot_surface(X_m, Y_m, width_of_confidence_interval.transpose(), cmap=cm.coolwarm, linewidth=0, antialiased=True)
#ax.invert_xaxis()
ax.set_xlabel("distance [cm]")
ax.set_ylabel("payload size [B]")
ax.set_zlabel("width of the 95% confidence interval [s]")
# Add a color bar which maps values to colors.
plt3D.colorbar(surf, shrink=0.5, aspect=5)
plt.show()
