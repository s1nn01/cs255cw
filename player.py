import random
import math

# The aim of this coursework is to implement the minimax algorithm to determine the next move for a game of Connect.
# The goal in Connect is for a player to create a line of the specified number of pieces, either horizontally, vertically or diagonally.
# It is a 2-player game with each player having their own type of piece, "X" and "O" in this instantiation.
# You will implement the strategy for the first player, who plays "X". The opponent, who always goes second, plays "O".
# The number of rows and columns in the board varies, as does the number of pieces required in a line to win.
# Each turn, a player must select a column in which to place a piece. The piece then falls to the lowest unfilled location.
# Rows and columns are indexed from 0. Thus, if at the start of the game you choose column 2, your piece will fall to row 0 of column 2. 
# If the opponent also selects column 2 their piece will end up in row 1 of column 2, and so on until column 2 is full (as determined
# by the number of rows). 
# Note that board locations are indexed in the data structure as [row][column]. However, you should primarily be using checkFull(), 
# checkSpace() etc. in board.py rather than interacting directly with the board.gameBoard structure.
# It is recommended that look at the comments in board.py to get a feel for how it is implemented. 
#
# Your task is to complete the two methods, 'getMove()' and 'getMoveAlphaBeta()'.
#
# getMove() should implement the minimax algorithm, with no pruning. It should return a number, between 0 and (maxColumns - 1), to
# select which column your next piece should be placed in. Remember that columns are zero indexed, and so if there are 4 columns in
# you must return 0, 1, 2 or 3. 
#
# getMoveAlphaBeta() should implement minimax with alpha-beta pruning. As before, it should return the column that your next
# piece should be placed in.
#
# The only imports permitted are those already imported. You may not use any additional resources. Doing so is likely to result in a 
# mark of zero. Also note that this coursework is NOT an exercise in Python proficiency, which is to say you are not expected to use the
# most "Pythonic" way of doing things. Your implementation should be readable and commented appropriately. Similarly, the code you are 
# given is intended to be readable rather than particularly efficient or "Pythonic".
#
# IMPORTANT: You MUST TRACK how many nodes you expand in your minimax and minimax with alpha-beta implementations.
# IMPORTANT: In your minimax with alpha-beta implementation, when pruning you MUST TRACK the number of times you prune.
class Player:
	
	def __init__(self, name):
		self.name = name
		self.numExpanded = 0 # Use this to track the number of nodes you expand
		self.numPruned = 0 # Use this to track the number of times you prune 

	def _opponent(self):
		"""return the opponent's piece type"""
		return "O" if self.name == "X" else "X"
	
	def legalMoves(self, gameBoard):
		"""return list of legal moves where columns are not full, a column is legal if it has space for at least one more piece"""
		return [c for c in range(gameBoard.numColumns) if gameBoard.colFills[c] < gameBoard.numRows]
	
	def terminalValue(self, gameBoard, me, opp, depth):
		"""
		checks if current board state is terminal (win/loss/draw)
		returns:
		- large positive value for a win
		- large negative value for a loss
		- 0 for a draw
		- None if game is not over
		depth adjustment allows preferring wins in fewer moves and losses are avoided for as long as possible
		Reference: Russell & Norvig (2010), Artificial Intelligence: A Modern Approach, Ch. 5
		"""
		if gameBoard.checkWin():
			winner = gameBoard.lastPlay[2]
			if winner == me:
				return 10**9 - depth # prefer faster wins - shorter paths
			elif winner == opp:
				return -10**9 + depth # prefer slower losses - longer paths 
		if gameBoard.checkFull():
			return 0 # draw
		return None # game is not over
	
	def scoreWindow(self, window, me, opp, winNum):
		""""
		evaluate a single window for tactical value
		scoring system based on connect4 heuristic from:
		- Victor, D. (2013). Connect-4 evaluation patterns
		  https://github.com/denkspuren/BitboardC4/blob/master/BitboardDesign.md
		args:
		- window: list of winNum positions 
		- me: player's piece type
		- opp: opponent's piece type
		- winNum: number of pieces in a line required to win
		returns:
		- weighted score for window based on piece configuration
		"""
		me_count = window.count(me)
		opp_count = window.count(opp)
		empty = window.count(" ")

		# window is blocked
		if me_count > 0 and opp_count > 0:
			return 0
		
		# immediate win/loss
		if me_count == winNum:
			return 10**8
		if opp_count == winNum:
			return -10**8
		
		# one piece away from win/loss
		if me_count == winNum - 1 and empty == 1:
			return 10**5
		if opp_count == winNum - 1 and empty == 1:
			return -10**5
		
		# two pieces away from win/loss
		if me_count == winNum - 2 and empty == 2:
			return 10**3
		if opp_count == winNum - 2 and empty == 2:
			return -10**3
		
		# single piece with room to grow
		if me_count == 1 and empty == winNum - 1:
			return 5
		if opp_count == 1 and empty == winNum - 1:
			return -5
		
		return 0
	
	def _heuristic(self, gameBoard, me, opp):
		"""
		heuristic evaluation of non-terminal board state
		evaluates board position by rewarding center column control and scoring all possible winning windows 
		weighted approach valyes patterns which are nearly complete lines, developing lines and center control in that order
		references: Russell & Norvig (2010): Heuristic evaluation functions for game trees
		args:
		- gameBoard: current board state
		- me: player's piece type
		- opp: opponent's piece type
		returns:
		- numeric score where positive favours me and negative favours opponent
		"""
		winNum = gameBoard.winNum
		rows = gameBoard.numRows
		cols = gameBoard.numColumns
		score = 0

		# center control: provides more winning opportunities, a piece in center can contribute to more winning lines diagonally/horizontally/vertically
		center = cols // 2
		for r in range(rows):
			if gameBoard.gameBoard[r][center].value == me:
				score += 3
			elif gameBoard.gameBoard[r][center].value == opp:
				score -= 3
		
		# horizontal and vertical scoring
		for r in range(rows):
			for c in range(cols - winNum + 1):
				window = [gameBoard.gameBoard[r][c + i].value for i in range(winNum)]
				score += self.scoreWindow(window, me, opp, winNum)

		for c in range(cols):
			for r in range(rows - winNum + 1):
				window = [gameBoard.gameBoard[r + i][c].value for i in range(winNum)]
				score += self.scoreWindow(window, me, opp, winNum)

		# bottom-left to top-right diagonal
		for r in range(rows - winNum + 1):
			for c in range(cols - winNum + 1):
				window = [gameBoard.gameBoard[r + i][c + i].value for i in range(winNum)]
				score += self.scoreWindow(window, me, opp, winNum)

		# top-left to bottom-right diagonal
		for r in range(winNum - 1, rows):
			for c in range(cols - winNum + 1):
				window = [gameBoard.gameBoard[r - i][c + i].value for i in range(winNum)]
				score += self.scoreWindow(window, me, opp, winNum)

		return score
	
	def orderedMoves(self, gameBoard, moves):
		"""
		order moves using center-first strategy to improve alpha-beta pruning efficiency
		move ordering is needed as good ordering can reduce effective branching factor and poor ordering would provide minimal benefit
		args:
		- gameBoard: current board state
		- moves: list of legal moves
		returns:
		- list of moves ordered by proximity to center column
		"""
		center = gameBoard.numColumns // 2
		return sorted(moves, key=lambda c: abs(c - center))
	
	def getMove(self, gameBoard, max_depth=7):
		"""
		minimax algorithm to select next move without alpha-beta pruning
		decision rule for minimising the possible loss for a worst case scenario, assumes opponent plays optimally
		algorithm: 
		- maximise player tries to maximise score
		- minimise opponent tries to minimise score
		- recursively explore all possible moves up to max_depth
		- use heuristic at leaf nodes to evaluate non-terminal states
		complexity:
		- time: O(b^d) where b is branching factor and d is depth
		- space: O(d) due to recursion stack
		args:
		- gameBoard: current board state
		- max_depth: maximum search depth for minimax
		returns:
		- column index for next best move
		"""
		# self.numExpanded = 0
		# self.numPruned = 0

		me = self.name 
		opp = self._opponent()

		MAX_DEPTH = max_depth

		def minimax(depth, maximizing):
			self.numExpanded += 1 # track node expansion
			# check for terminal state
			term = self.terminalValue(gameBoard, me, opp, depth)
			if term is not None:
				return term
			# reached max depth, evaluate heuristically
			if depth == 0:
				return self._heuristic(gameBoard, me, opp)

			# get possible moves
			moves = self.orderedMoves(gameBoard, self.legalMoves(gameBoard))
			if not moves:
				return 0 # no legal moves
			if maximizing:
				# maximising player, choose move with lowest value
				best = -10**18
				for col in moves:
					gameBoard.addPiece(col, me)
					val = minimax(depth - 1, False)
					gameBoard.removePiece(col)
					if val > best:
						best = val
				return best
			else:
				# minimising opponent, choose move with highest value
				best = 10**18
				for col in moves:
					gameBoard.addPiece(col, opp)
					val = minimax(depth - 1, True)
					gameBoard.removePiece(col)
					if val < best:
						best = val
				return best
		
		# find best move for current player
		best_move = None
		best_value = -10**18
		for col in self.orderedMoves(gameBoard, self.legalMoves(gameBoard)):
			gameBoard.addPiece(col, me)
			val = minimax(MAX_DEPTH - 1, False)
			gameBoard.removePiece(col)
			if val > best_value:
				best_value = val
				best_move = col
		
		# if none found, return first legal move
		if best_move is None:
			moves = self.orderedMoves(gameBoard, self.legalMoves(gameBoard))
			return moves[0] if moves else 0

		return best_move
	def getMoveAlphaBeta(self, gameBoard, max_depth=5):
		"""
		minimax algorithm with alpha-beta pruning to select next move
		alpha-beta pruning is an optimization technique for minimax that eliminates branches that cannot possibly influence the final decision, it maintains alpha and beta values. 
		alpha: best value maximising player can guarantee - lower bound
		beta: best value minimising player can guarantee - upper bound
		if at any point beta <= alpha, prune remaining branches (cut off)
		- can search deeper in same time compared to minimax, reduced complexity to O(b^(d/2)) in best case
		args:
		- gameBoard: current board state
		- max_depth: maximum search depth for minimax with alpha-beta pruning
		returns:
		- column index for next best move
		references: 
		- Knuth & Moore (1975): "An analysis of alpha-beta pruning"
		  https://www.sciencedirect.com/science/article/pii/0004370275900193
		- https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
		- Video explanation: https://www.youtube.com/watch?v=l-hh51ncgDI
		"""
		# self.numExpanded = 0
		# self.numPruned = 0

		me = self.name
		opp = self._opponent()

		MAX_DEPTH = max_depth

		def alphabeta(depth, alpha, beta, maximizing):
			self.numExpanded += 1 # track node expansion
			# check for terminal state
			term = self.terminalValue(gameBoard, me, opp, depth)
			if term is not None:
				return term
			# reached max depth, evaluate heuristically
			if depth == 0:
				return self._heuristic(gameBoard, me, opp)

			# get possible moves
			moves = self.orderedMoves(gameBoard, self.legalMoves(gameBoard))
			if not moves:
				return 0 # no legal moves 
			if maximizing:
				# maximising player, choose move with lowest value
				best = -10**18
				for col in moves:
					gameBoard.addPiece(col, me)
					val = alphabeta(depth - 1, alpha, beta, False)
					gameBoard.removePiece(col)
					if val > best:
						best = val
					if best > alpha:
						alpha = best # update lower bound
					# beta cut-off: minimising player will avoid this branch - have better options
					if beta <= alpha:
						self.numPruned += 1 # track pruning
						break # prune remaining branches
				return best
			else:
				# minimising opponent, choose move with highest value
				best = 10**18
				for col in moves:
					gameBoard.addPiece(col, opp)
					val = alphabeta(depth - 1, alpha, beta, True)
					gameBoard.removePiece(col)
					if val < best:
						best = val
					if best < beta:
						beta = best # update upper bound
					# alpha cut-off: maximising player will avoid this branch - have better options
					if beta <= alpha:
						self.numPruned += 1 # track pruning
						break # prune remaining branches
				return best
			
		# find best move for current player
		best_move = None
		best_value = -10**18
		alpha = -10**18
		beta = 10**18
		for col in self.orderedMoves(gameBoard, self.legalMoves(gameBoard)):
			gameBoard.addPiece(col, me)
			val = alphabeta(MAX_DEPTH - 1, alpha, beta, False)
			gameBoard.removePiece(col)
			if val > best_value:
				best_value = val
				best_move = col
			if best_value > alpha:
				alpha = best_value # update at root level
		# if none found, return first legal move
		if best_move is None:
			moves = self.orderedMoves(gameBoard, self.legalMoves(gameBoard))
			return moves[0] if moves else 0
		
		return best_move

