import matplotlib.pyplot as plt
from pathlib import Path

plot_folder = Path("./")

configs = ["4×4,3", "5×6,4", "6×7,4", "6×7,3"]

minimax_nodes = [3312, 53344, 128616, 74487]
ab_nodes      = [2569, 50789, 149738, 36281]

x = range(len(configs))

fig = plt.figure()
plt.ylabel("Nodes expanded (mean)")
plt.xlabel("Configuration")
plt.plot(x, minimax_nodes, marker='o', linestyle='dashed', label="Minimax")
plt.plot(x, ab_nodes, marker='o', linestyle='dotted', label="Alpha-Beta")
plt.xticks(x, configs)
plt.legend(loc='upper left')
plt.tight_layout()

plt.savefig(plot_folder/"comparison_nodes.pdf")
plt.close(fig)
