import matplotlib.pyplot as plt
import numpy as np

# Your data
configs = ['4×4\nwin=3', '4×5\nwin=3', '5×6\nwin=4', '5×6\nwin=3', '6×7\nwin=4', '6×7\nwin=3']
configs_short = ['4×4, 3', '4×5, 3', '5×6, 4', '5×6, 3', '6×7, 4', '6×7, 3']
minimax_nodes = [3322, 10516, 56916, 31007, 140446, 74875]
minimax_std = [483, 1549, 7597, 6225, 15500, 17423]
alphabeta_nodes = [862, 1629, 8527, 3051, 12744, 5263]
alphabeta_std = [36, 261, 1969, 365, 2097, 905]
pruned = [172, 376, 1505, 699, 2191, 1096]
speedups = [3.48, 7.79, 7.63, 13.04, 12.49, 18.50]
reductions = [74.0, 84.5, 85.0, 90.2, 90.9, 93.0]

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.family'] = 'serif'

def create_figure1():
    """Node Expansion Comparison - Bar Chart"""
    x = np.arange(len(configs))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    bars1 = ax.bar(x - width/2, minimax_nodes, width, 
                   yerr=minimax_std, capsize=5,
                   label='Minimax (no pruning)', 
                   color='#e74c3c', edgecolor='black', linewidth=1.2)
    
    bars2 = ax.bar(x + width/2, alphabeta_nodes, width,
                   yerr=alphabeta_std, capsize=5,
                   label='Alpha-Beta (with pruning)', 
                   color='#3498db', edgecolor='black', linewidth=1.2)
    
    ax.set_xlabel('Board Configuration', fontsize=14, fontweight='bold')
    ax.set_ylabel('Nodes Expanded (mean ± std)', fontsize=14, fontweight='bold')
    ax.set_title('Node Expansion Comparison: Minimax vs Alpha-Beta Pruning\n(Search Depth = 5)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(configs, fontsize=11)
    ax.legend(fontsize=12, loc='upper left')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('figure1_node_comparison.pdf', dpi=300, bbox_inches='tight')
    print("✓ Figure 1 saved!")
    plt.close()

def create_figure2():
    """Reduction Percentage"""
    colors = plt.cm.Greens(np.linspace(0.5, 0.9, len(reductions)))
    
    fig, ax = plt.subplots(figsize=(12, 7))
    bars = ax.bar(configs, reductions, color=colors, edgecolor='black', linewidth=1.5)
    
    ax.set_xlabel('Board Configuration', fontsize=14, fontweight='bold')
    ax.set_ylabel('Node Reduction (%)', fontsize=14, fontweight='bold')
    ax.set_title('Alpha-Beta Pruning Efficiency Increases with Board Complexity', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3)
    
    for bar, reduction in zip(bars, reductions):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1.5,
                f'{reduction:.1f}%',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('figure2_reduction_percentage.pdf', dpi=300, bbox_inches='tight')
    print("✓ Figure 2 saved!")
    plt.close()

def create_figure3():
    """Scaling Analysis - Log Scale"""
    x = np.arange(len(configs_short))
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    ax.plot(x, minimax_nodes, 'o-', linewidth=3, markersize=10, 
            color='#e74c3c', label='Minimax (no pruning)', 
            markeredgecolor='black', markeredgewidth=1.5)
    ax.plot(x, alphabeta_nodes, 's-', linewidth=3, markersize=10, 
            color='#3498db', label='Alpha-Beta (with pruning)', 
            markeredgecolor='black', markeredgewidth=1.5)
    
    ax.set_yscale('log')
    ax.set_xlabel('Board Configuration', fontsize=14, fontweight='bold')
    ax.set_ylabel('Nodes Expanded (log scale)', fontsize=14, fontweight='bold')
    ax.set_title('Exponential Scaling: Minimax vs Alpha-Beta', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(configs_short, fontsize=11)
    ax.legend(fontsize=12, loc='upper left')
    ax.grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    plt.savefig('figure3_scaling_logscale.pdf', dpi=300, bbox_inches='tight')
    print("✓ Figure 3 saved!")
    plt.close()

# Generate all figures
print("Generating figures...")
create_figure1()
create_figure2()
create_figure3()
print("\n✓ All figures generated successfully!")
print("Files created: figure1_node_comparison.pdf, figure2_reduction_percentage.pdf, figure3_scaling_logscale.pdf")