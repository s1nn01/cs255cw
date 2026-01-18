import matplotlib.pyplot as plt
from pathlib import Path

plot_folder = Path("./")

configs = ["4×4,3", "5×6,4", "6×7,4", "6×7,3"]
xpoints = list(range(1, len(configs)+1))
nodes = [2569, 50789, 149738, 36281]   # alpha-beta nodes (means)

fig = plt.figure()
plt.ylabel('Nodes expanded')
plt.xlabel('Configuration')
plt.plot(xpoints, nodes, color='#009999', marker='o', linestyle='dashed', label="Alpha-beta nodes")
plt.xticks(xpoints, configs)
plt.legend(loc='upper left')

filename = plot_folder / "ab_nodes.pdf"
plt.savefig(filename)
plt.close(fig)

