import board
import game
import player
import randomPlayer
import csv
import time

def run_experiments(num_runs=10):
    """
    Run comprehensive experiments and save data to CSV files for plotting.
    """
    
    # Experiment 1: Compare Minimax vs Alpha-Beta across different board sizes
    print("Running Experiment 1: Board Size Impact...")
    
    board_configs = [
        (4, 4, 3),
        (4, 5, 3),
        (5, 6, 4),
        (6, 7, 4),
    ]
    
    with open('board_size_comparison.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['BoardSize', 'Algorithm', 'NodesExpanded', 'Pruned', 'Time', 'Result'])
        
        for rows, cols, win_num in board_configs:
            board_size = f"{rows}x{cols}"
            print(f"  Testing {board_size}...")
            
            for run in range(num_runs):
                # Minimax
                p1 = player.Player("X")
                p2 = randomPlayer.RandomPlayer("O", run)
                g = game.Game(p1, p2, rows, cols, win_num)
                start = time.time()
                result = g.playGame(False)
                elapsed = time.time() - start
                writer.writerow([board_size, 'Minimax', p1.numExpanded, 0, elapsed, result])
                
                # Alpha-Beta
                p1 = player.Player("X")
                p2 = randomPlayer.RandomPlayer("O", run)
                g = game.Game(p1, p2, rows, cols, win_num)
                start = time.time()
                result = g.playGame(True)
                elapsed = time.time() - start
                writer.writerow([board_size, 'AlphaBeta', p1.numExpanded, p1.numPruned, elapsed, result])
    
    print("  Saved to: board_size_comparison.csv")
    
    # Experiment 2: Win requirement impact
    print("\nRunning Experiment 2: Win Requirement Impact...")
    
    with open('win_requirement_impact.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['WinRequirement', 'NodesExpanded', 'Pruned', 'Time', 'Result'])
        
        for win_num in [3, 4, 5]:
            print(f"  Testing win requirement {win_num}...")
            for run in range(num_runs):
                p1 = player.Player("X")
                p2 = randomPlayer.RandomPlayer("O", run)
                g = game.Game(p1, p2, 5, 6, win_num)
                start = time.time()
                result = g.playGame(True)
                elapsed = time.time() - start
                writer.writerow([win_num, p1.numExpanded, p1.numPruned, elapsed, result])
    
    print("  Saved to: win_requirement_impact.csv")
    
    # Experiment 3: Pruning efficiency over many games
    print("\nRunning Experiment 3: Pruning Efficiency...")
    
    with open('pruning_efficiency.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['GameNumber', 'MinimaxNodes', 'AlphaBetaNodes', 'PruneCount', 'ReductionPercent'])
        
        for run in range(num_runs):
            print(f"  Game {run + 1}/{num_runs}...")
            
            # Minimax
            p1_mm = player.Player("X")
            p2 = randomPlayer.RandomPlayer("O", run + 1000)
            g1 = game.Game(p1_mm, p2, 5, 6, 4)
            g1.playGame(False)
            
            # Alpha-Beta
            p1_ab = player.Player("X")
            p2 = randomPlayer.RandomPlayer("O", run + 1000)
            g2 = game.Game(p1_ab, p2, 5, 6, 4)
            g2.playGame(True)
            
            reduction = ((p1_mm.numExpanded - p1_ab.numExpanded) / p1_mm.numExpanded * 100) if p1_mm.numExpanded > 0 else 0
            writer.writerow([run + 1, p1_mm.numExpanded, p1_ab.numExpanded, p1_ab.numPruned, reduction])
    
    print("  Saved to: pruning_efficiency.csv")
    
    # Experiment 4: Depth analysis (if you want to test different depths)
    print("\nRunning Experiment 4: Search Depth Analysis...")
    print("  (Requires modifying MAX_DEPTH in player.py)")
    print("  Skipping for now - modify player.py to test different depths")
    
    print("\n" + "=" * 80)
    print("All experiments complete!")
    print("CSV files created for plotting in your report:")
    print("  - board_size_comparison.csv")
    print("  - win_requirement_impact.csv")
    print("  - pruning_efficiency.csv")
    print("=" * 80)

if __name__ == "__main__":
    run_experiments(num_runs=10)