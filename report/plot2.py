import matplotlib.pyplot as plt
from pathlib import Path

plot_folder = Path("./")

configs = ["4×4,3", "5×6,4", "6×7,4", "6×7,3"]
xpoints = list(range(1, len(configs)+1))
pruning = [28.1, 19.7, 17.3, 25.1]

fig = plt.figure()
plt.ylabel('Pruning Rate (%)')
plt.xlabel('Configuration')
plt.plot(xpoints, pruning, color='#ff9933', marker='o', linestyle='dotted', label="Pruning %")
plt.xticks(xpoints, configs)
plt.legend(loc='upper left')
plt.errorbar(xpoints, nodes, yerr=nodes_sd, fmt='o--', color='#009999', capsize=3, label='Alpha-beta nodes')


filename = plot_folder / "ab_pruning.pdf"
plt.savefig(filename)
plt.close(fig)
