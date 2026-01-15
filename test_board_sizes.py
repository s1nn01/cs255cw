import board
import game
import player
import randomPlayer
import time

def test_single_game(rows, cols, win_num, use_alpha_beta):
    """Run a single game and return statistics."""
    p1 = player.Player("X")
    p2 = randomPlayer.RandomPlayer("O", 42)
    g = game.Game(p1, p2, rows, cols, win_num)
    
    start = time.time()
    result = g.playGame(use_alpha_beta)
    elapsed = time.time() - start
    
    return {
        'result': result,
        'expanded': p1.numExpanded,
        'pruned': p1.numPruned,
        'time': elapsed
    }

print("=" * 80)
print("BOARD SIZE IMPACT ANALYSIS")
print("=" * 80)
print()

# Test different board sizes
board_sizes = [
    (4, 4, 3, "Very Small"),
    (4, 5, 3, "Small"),
    (5, 6, 4, "Standard"),
    (6, 7, 4, "Large"),
]

print("Testing Alpha-Beta on different board sizes:")
print("-" * 80)
print(f"{'Config':<20} {'Size':<10} {'Result':<8} {'Nodes':<12} {'Pruned':<10} {'Time (s)'}")
print("-" * 80)

for rows, cols, win_num, description in board_sizes:
    stats = test_single_game(rows, cols, win_num, True)
    result_str = {1: "WIN", -1: "LOSS", 0: "DRAW"}[stats['result']]
    print(f"{description:<20} {rows}x{cols}    {result_str:<8} {stats['expanded']:<12} {stats['pruned']:<10} {stats['time']:.3f}")

print()
print("\nTesting different Win Requirements (5x6 board):")
print("-" * 80)
print(f"{'Win Req':<10} {'Result':<8} {'Nodes':<12} {'Pruned':<10} {'Time (s)'}")
print("-" * 80)

for win_num in [3, 4, 5]:
    stats = test_single_game(5, 6, win_num, True)
    result_str = {1: "WIN", -1: "LOSS", 0: "DRAW"}[stats['result']]
    print(f"{win_num:<10} {result_str:<8} {stats['expanded']:<12} {stats['pruned']:<10} {stats['time']:.3f}")

print("\n" + "=" * 80)