import matplotlib.pyplot as plt
from pathlib import Path

plot_folder = Path("./")

# Your depth scaling data
depths = [3, 4, 5, 6, 7]
nodes_mean = [217, 476, 1658, 2877, 6700]
nodes_std = [33, 67, 292, 599, 1079]
time_mean = [0.002, 0.004, 0.012, 0.015, 0.036]
time_std = [0.000, 0.001, 0.002, 0.004, 0.006]

x = range(len(depths))

# Figure 1: Nodes vs Depth
fig = plt.figure()
plt.ylabel("Nodes expanded (mean)")
plt.xlabel("Search Depth")
plt.errorbar(depths, nodes_mean, yerr=nodes_std, marker='o', 
             linestyle='dashed', capsize=5, label="Alpha-Beta pruning")
plt.xticks(depths)
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig(plot_folder / "depth_scaling_nodes.pdf")
plt.close(fig)

# Figure 2: Time vs Depth
fig = plt.figure()
plt.ylabel("Time (seconds, mean)")
plt.xlabel("Search Depth")
plt.errorbar(depths, time_mean, yerr=time_std, marker='o', 
             linestyle='dashed', capsize=5, label="Alpha-Beta pruning")
plt.xticks(depths)
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig(plot_folder / "depth_scaling_time.pdf")
plt.close(fig)
