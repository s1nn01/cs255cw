import board
import game
import player
import randomPlayer

print("=" * 60)
print("TEST 1: Minimax (no pruning) vs Random Player")
print("=" * 60)

p1 = player.Player("X")
p2 = randomPlayer.RandomPlayer("O", 42)
g = game.Game(p1, p2, 5, 6, 4)
result = g.playGame(False)  # False = no alpha-beta
print(f"Result: {result} (1=win, -1=loss, 0=draw)")
print()

print("=" * 60)
print("TEST 2: Alpha-Beta Pruning vs Random Player")
print("=" * 60)

p1 = player.Player("X")
p2 = randomPlayer.RandomPlayer("O", 42)
g = game.Game(p1, p2, 5, 6, 4)
result = g.playGame(True)  # True = use alpha-beta
print(f"Result: {result} (1=win, -1=loss, 0=draw)")
print()

print("=" * 60)
print("TEST 3: Verify Alpha-Beta Prunes")
print("=" * 60)
print("Alpha-beta should expand fewer nodes than minimax")

p1_minimax = player.Player("X")
p2 = randomPlayer.RandomPlayer("O", 100)
g1 = game.Game(p1_minimax, p2, 5, 6, 4)
g1.playGame(False)
minimax_expanded = p1_minimax.numExpanded

p1_ab = player.Player("X")
p2 = randomPlayer.RandomPlayer("O", 100)
g2 = game.Game(p1_ab, p2, 5, 6, 4)
g2.playGame(True)
ab_expanded = p1_ab.numExpanded
ab_pruned = p1_ab.numPruned

print(f"Minimax expanded: {minimax_expanded} nodes")
print(f"Alpha-Beta expanded: {ab_expanded} nodes")
print(f"Alpha-Beta pruned: {ab_pruned} times")
print(f"Reduction: {((minimax_expanded - ab_expanded) / minimax_expanded * 100):.1f}%")