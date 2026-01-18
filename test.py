import player
import randomPlayer
import game
import time
import statistics

configs = [
    (4, 4, 3), 
    (5, 6, 4),
    (6, 7, 4),
    (6, 7, 3),
]

for rows, cols, win_len in configs:
    print(f"\n{'='*50}")
    print(f"=== Testing {rows}×{cols}, win={win_len} ===")
    print(f"{'='*50}")
    
    results_ab = []
    results_mm = []
    
    for run in range(30):  # Changed to 10 for better statistics
        seed = 42 + run
        
        # Test MINIMAX first (without pruning)
        p1 = player.Player("X")
        p2 = player.Player("O")  # Use seed from loop!
        g = game.Game(p1, p2, rows, cols, win_len)
        
        start = time.time()
        winner_mm = g.playGame(False)  # False = NO pruning
        mm_time = time.time() - start
        
        results_mm.append({
            'expanded': p1.numExpanded,
            'pruned': p1.numPruned,  # Should always be 0
            'time': mm_time,
        })
        
        # Test ALPHA-BETA (with same seed for fair comparison)
        p1 = player.Player("X")
        p2 = player.Player("O")  # SAME seed as minimax!
        g = game.Game(p1, p2, rows, cols, win_len)
        
        start = time.time()
        winner_ab = g.playGame(True)  # True = alpha-beta
        ab_time = time.time() - start
        
        results_ab.append({
            'expanded': p1.numExpanded,
            'pruned': p1.numPruned,
            'time': ab_time,
        })
        
        # Print per-game comparison
        reduction = (1 - results_ab[-1]['expanded'] / results_mm[-1]['expanded']) * 100
        print(f"Game {run+1}: MM={results_mm[-1]['expanded']:6d} nodes, "
              f"AB={results_ab[-1]['expanded']:6d} nodes, "
              f"Reduction={reduction:5.1f}%")
    
    # Calculate statistics
    mm_nodes = [r['expanded'] for r in results_mm]
    ab_nodes = [r['expanded'] for r in results_ab]
    ab_pruned = [r['pruned'] for r in results_ab]
    mm_time = [r['time'] for r in results_mm]
    ab_time = [r['time'] for r in results_ab]
    
    # Calculate mean reduction
    mean_reduction = (1 - statistics.mean(ab_nodes) / statistics.mean(mm_nodes)) * 100
    
    print(f"\n{'='*50}")
    print(f"SUMMARY")
    print(f"{'='*50}")
    print(f"Minimax (no pruning):")
    print(f"  Nodes: {statistics.mean(mm_nodes):.0f} ± {statistics.stdev(mm_nodes):.0f}")
    print(f"  Time:  {statistics.mean(mm_time):.3f}s ± {statistics.stdev(mm_time):.3f}s")
    
    print(f"\nAlpha-Beta (with pruning):")
    print(f"  Nodes:  {statistics.mean(ab_nodes):.0f} ± {statistics.stdev(ab_nodes):.0f}")
    print(f"  Pruned: {statistics.mean(ab_pruned):.0f} ± {statistics.stdev(ab_pruned):.0f}")
    print(f"  Pruning %: {(statistics.mean(ab_pruned) / statistics.mean(ab_nodes) * 100):.1f}%")
    print(f"  Time:  {statistics.mean(ab_time):.3f}s ± {statistics.stdev(ab_time):.3f}s")
    
    print(f"\nComparison:")
    print(f"  Node Reduction: {mean_reduction:.1f}%")
    print(f"  Speedup: {statistics.mean(mm_time) / statistics.mean(ab_time):.2f}×")