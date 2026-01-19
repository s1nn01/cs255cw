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
    print(f"\n=== Win Rate Test: {rows}×{cols}, win={win_len} ===")
    
    wins = 0
    losses = 0
    draws = 0
    
    for run in range(10):
        p1 = player.Player("X")
        p2 = randomPlayer.RandomPlayer("O", 42 + run)
        g = game.Game(p1, p2, rows, cols, win_len)
        
        # Capture printed output to detect win/loss
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        
        g.playGame(True)  # Alpha-beta
        
        output = buffer.getvalue()
        sys.stdout = old_stdout
        
        if "You Win!" in output:
            wins += 1
        elif "You Lose!" in output:
            losses += 1
        elif "Draw" in output or "Tie" in output:
            draws += 1
        
        print(f"Game {run+1}: {output.strip().split()[-1] if output.strip() else 'Unknown'}")
    
    print(f"\nResults: {wins} wins, {losses} losses, {draws} draws")
    print(f"Win Rate: {wins/10*100:.1f}%")
