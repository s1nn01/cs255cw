import board
import game
import player
import randomPlayer
from datetime import datetime
import time

def run_multiple_games(num_games, board_config, use_alpha_beta, seed_start=0):
    """
    Run multiple games and collect statistics.
    board_config: (rows, cols, win_num)
    """
    rows, cols, win_num = board_config
    
    wins = 0
    losses = 0
    draws = 0
    total_expanded = 0
    total_pruned = 0
    expanded_per_game = []
    pruned_per_game = []
    
    start_time = time.time()
    
    for i in range(num_games):
        p1 = player.Player("X")
        seed = seed_start + i
        p2 = randomPlayer.RandomPlayer("O", seed)
        g = game.Game(p1, p2, rows, cols, win_num)
        
        result = g.playGame(use_alpha_beta)
        
        if result == 1:
            wins += 1
        elif result == -1:
            losses += 1
        else:
            draws += 1
        
        total_expanded += p1.numExpanded
        expanded_per_game.append(p1.numExpanded)
        
        if use_alpha_beta:
            total_pruned += p1.numPruned
            pruned_per_game.append(p1.numPruned)
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    # Calculate statistics
    avg_expanded = total_expanded / num_games
    avg_pruned = total_pruned / num_games if use_alpha_beta else 0
    
    # Calculate standard deviation
    import math
    if len(expanded_per_game) > 1:
        variance = sum((x - avg_expanded) ** 2 for x in expanded_per_game) / (len(expanded_per_game) - 1)
        std_expanded = math.sqrt(variance)
    else:
        std_expanded = 0
    
    return {
        'wins': wins,
        'losses': losses,
        'draws': draws,
        'win_rate': wins / num_games * 100,
        'avg_expanded': avg_expanded,
        'std_expanded': std_expanded,
        'avg_pruned': avg_pruned,
        'total_time': elapsed,
        'avg_time_per_game': elapsed / num_games
    }

# Test configurations
print("=" * 80)
print("PERFORMANCE COMPARISON: Minimax vs Alpha-Beta")
print("=" * 80)
print()

configs = [
    (5, 6, 4, "Standard 5x6, Win=4"),
    (4, 5, 3, "Smaller 4x5, Win=3"),
    (4, 4, 4, "Tiny 4x4, Win=4"),
    (5, 6, 3, "Standard 5x6, Win=3 (easier)"),
]

num_games = 10

for rows, cols, win_num, description in configs:
    print(f"\n{'=' * 80}")
    print(f"Configuration: {description}")
    print(f"Board: {rows} rows x {cols} columns, Win: {win_num} in a row")
    print('=' * 80)
    
    # Test minimax
    print("\nMinimax (no pruning):")
    minimax_stats = run_multiple_games(num_games, (rows, cols, win_num), False)
    print(f"  Win rate: {minimax_stats['win_rate']:.1f}%")
    print(f"  Avg nodes expanded: {minimax_stats['avg_expanded']:.0f} ± {minimax_stats['std_expanded']:.0f}")
    print(f"  Avg time per game: {minimax_stats['avg_time_per_game']:.2f}s")
    print(f"  Total time: {minimax_stats['total_time']:.2f}s")
    
    # Test alpha-beta
    print("\nAlpha-Beta Pruning:")
    ab_stats = run_multiple_games(num_games, (rows, cols, win_num), True)
    print(f"  Win rate: {ab_stats['win_rate']:.1f}%")
    print(f"  Avg nodes expanded: {ab_stats['avg_expanded']:.0f} ± {ab_stats['std_expanded']:.0f}")
    print(f"  Avg times pruned: {ab_stats['avg_pruned']:.0f}")
    print(f"  Avg time per game: {ab_stats['avg_time_per_game']:.2f}s")
    print(f"  Total time: {ab_stats['total_time']:.2f}s")
    
    # Comparison
    print("\nComparison:")
    if minimax_stats['avg_expanded'] > 0:
        reduction = (1 - ab_stats['avg_expanded'] / minimax_stats['avg_expanded']) * 100
        print(f"  Node expansion reduction: {reduction:.1f}%")
    if minimax_stats['total_time'] > 0:
        speedup = minimax_stats['total_time'] / ab_stats['total_time']
        print(f"  Speedup: {speedup:.2f}x")

print("\n" + "=" * 80)
print("Testing complete!")
print("=" * 80)