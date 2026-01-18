import player
import randomPlayer
import game
import time
import statistics

print("=== Alpha-Beta Depth Scaling Test ===\n")

# Small board for testing multiple depths
rows, cols, win_len = 4, 5, 3

depths = [3, 4, 5, 6, 7]

for depth in depths:
    print(f"Testing depth {depth}...")
    
    # Temporarily modify player.py to use this depth
    # OR modify your code to accept depth as parameter
    
    results = []
    for run in range(30):
        p1 = player.Player("X")
        p2 = player.Player("O")
        g = game.Game(p1, p2, rows, cols, win_len)
        
        # You need to modify getMoveAlphaBeta to accept depth parameter
        # For now, manually change MAX_DEPTH in player.py for each test
        
        start = time.time()
        g.playGame(True)
        elapsed = time.time() - start
        
        results.append({
            'nodes': p1.numExpanded,
            'pruned': p1.numPruned,
            'time': elapsed
        })
    
    nodes_mean = statistics.mean([r['nodes'] for r in results])
    nodes_std = statistics.stdev([r['nodes'] for r in results])
    time_mean = statistics.mean([r['time'] for r in results])
    
    print(f"Depth {depth}: {nodes_mean:.0f} ± {nodes_std:.0f} nodes, {time_mean:.3f}s")
# ```

# **Expected results to record:**
# ```
# Alpha-Beta Depth Scaling (4×5, win=3):
# - Depth 3: ~400 nodes, 0.003s
# - Depth 4: ~800 nodes, 0.006s
# - Depth 5: ~1,600 nodes, 0.011s
# - Depth 6: ~3,500 nodes, 0.025s
# - Depth 7: ~8,000 nodes, 0.055s