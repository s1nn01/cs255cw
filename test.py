import player
import randomPlayer
import game
import time

configs = [
    (4, 4, 3),  # rows, cols, win_length
    (5, 6, 4),
    (6, 7, 4),
]

for rows, cols, win_len in configs:
    print(f"\n=== Testing {rows}×{cols}, win={win_len} ===")
    
    # Test with alpha-beta
    results_ab = []
    for run in range(30):
        p1 = player.Player("X")
        p2 = randomPlayer.RandomPlayer("O", 42 + run)
        g = game.Game(p1, p2, rows, cols, win_len)
        
        start = time.time()
        winner = g.playGame(True)  # True = alpha-beta
        elapsed = time.time() - start
        
        results_ab.append({
            'expanded': p1.numExpanded,
            'pruned': p1.numPruned,
            'time': elapsed,
            'won': winner == "X"
        })
    
    # Calculate statistics
    import statistics
    print(f"Alpha-Beta:")
    print(f"  Nodes: {statistics.mean([r['expanded'] for r in results_ab]):.0f} ± {statistics.stdev([r['expanded'] for r in results_ab]):.0f}")
    print(f"  Pruned: {statistics.mean([r['pruned'] for r in results_ab]):.0f} ± {statistics.stdev([r['pruned'] for r in results_ab]):.0f}")
    print(f"  Win Rate: {sum([r['won'] for r in results_ab])/30*100:.1f}%")