import board
import game
import player
import randomPlayer

print("Quick Sanity Check")
print("=" * 60)

# Test 1: Does it win?
print("\nTest 1: Can it beat random player?")
wins = 0
for i in range(5):
    p1 = player.Player("X")
    p2 = randomPlayer.RandomPlayer("O", i)
    g = game.Game(p1, p2, 5, 6, 4)
    result = g.playGame(True)
    if result == 1:
        wins += 1
print(f"Result: Won {wins}/5 games")

# Test 2: Does alpha-beta prune?
print("\nTest 2: Does alpha-beta actually prune?")
p1 = player.Player("X")
p2 = randomPlayer.RandomPlayer("O", 42)
g = game.Game(p1, p2, 5, 6, 4)
g.playGame(True)
print(f"Nodes expanded: {p1.numExpanded}")
print(f"Times pruned: {p1.numPruned}")
if p1.numPruned > 0:
    print("✓ Alpha-beta is pruning!")
else:
    print("✗ WARNING: No pruning detected!")

# Test 3: Does alpha-beta expand fewer nodes?
print("\nTest 3: Does alpha-beta expand fewer nodes than minimax?")
p1_mm = player.Player("X")
p2 = randomPlayer.RandomPlayer("O", 42)
g1 = game.Game(p1_mm, p2, 5, 6, 4)
g1.playGame(False)

p1_ab = player.Player("X")
p2 = randomPlayer.RandomPlayer("O", 42)
g2 = game.Game(p1_ab, p2, 5, 6, 4)
g2.playGame(True)

print(f"Minimax nodes: {p1_mm.numExpanded}")
print(f"Alpha-Beta nodes: {p1_ab.numExpanded}")
if p1_ab.numExpanded < p1_mm.numExpanded:
    reduction = (1 - p1_ab.numExpanded/p1_mm.numExpanded) * 100
    print(f"✓ Alpha-beta is more efficient! ({reduction:.1f}% reduction)")
else:
    print("✗ WARNING: Alpha-beta not reducing node count!")

print("\n" + "=" * 60)
print("Quick test complete!")