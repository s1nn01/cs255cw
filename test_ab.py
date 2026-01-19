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
    
    results = []
    for run in range(10):
        p1 = player.Player("X")
        p2 = randomPlayer.RandomPlayer("O", 42 + run)
        g = game.Game(p1, p2, rows, cols, win_len)
        
        # Monkey-patch the getMoveAlphaBeta method to use custom depth
        original_method = p1.getMoveAlphaBeta
        p1.getMoveAlphaBeta = lambda gb: original_method(gb, max_depth=depth)
        
        start = time.time()
        g.playGame(True)  # Uses alpha-beta
        elapsed = time.time() - start
        
        results.append({
            'nodes': p1.numExpanded,
            'pruned': p1.numPruned,
            'time': elapsed
        })
    
    nodes_mean = statistics.mean([r['nodes'] for r in results])
    nodes_std = statistics.stdev([r['nodes'] for r in results])
    pruned_mean = statistics.mean([r['pruned'] for r in results])
    time_mean = statistics.mean([r['time'] for r in results])
    time_std = statistics.stdev([r['time'] for r in results])
    
    print(f"Depth {depth}: {nodes_mean:.0f} ± {nodes_std:.0f} nodes, "
          f"{pruned_mean:.0f} pruned, {time_mean:.3f}s ± {time_std:.3f}s\n")
