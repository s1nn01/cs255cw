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
		return "O" if self.name == "X" else "X"
	
	def legalMoves(self, gameBoard):
		return [c for c in range(gameBoard.numColumns) if gameBoard.colFills[c] < gameBoard.numRows]
	
	def terminalValue(self, gameBoard, me, opp, depth):
		if gameBoard.checkWin():
			winner = gameBoard.lastPlay[2]
			if winner == me:
				return 10**9 - depth
			elif winner == opp:
				return -10**9 + depth
		if gameBoard.checkFull():
			return 0
		return None
	
	def scoreWindow(self, window, me, opp, winNum):
		me_count = window.count(me)
		opp_count = window.count(opp)
		empty = window.count(" ")

		if me_count > 0 and opp_count > 0:
			return 0
		
		if me_count == winNum:
			return 10**8
		if opp_count == winNum:
			return -10**8
		
		if me_count == winNum - 1 and empty == 1:
			return 10**5
		if opp_count == winNum - 1 and empty == 1:
			return -10**5
		
		if me_count == winNum - 2 and empty == 2:
			return 10**3
		if opp_count == winNum - 2 and empty == 2:
			return -10**3
		
		if me_count == 1 and empty == winNum - 1:
			return 5
		if opp_count == 1 and empty == winNum - 1:
			return -5
		
		return 0
	
	def _heuristic(self, gameBoard, me, opp):
		winNum = gameBoard.winNum
		rows = gameBoard.numRows
		cols = gameBoard.numColumns
		score = 0

		center = cols // 2
		for r in range(rows):
			if gameBoard.gameBoard[r][center].value == me:
				score += 3
			elif gameBoard.gameBoard[r][center].value == opp:
				score -= 3

		for r in range(rows):
			for c in range(cols - winNum + 1):
				window = [gameBoard.gameBoard[r][c + i].value for i in range(winNum)]
				score += self.scoreWindow(window, me, opp, winNum)

		for c in range(cols):
			for r in range(rows - winNum + 1):
				window = [gameBoard.gameBoard[r + i][c].value for i in range(winNum)]
				score += self.scoreWindow(window, me, opp, winNum)

		for r in range(rows - winNum + 1):
			for c in range(cols - winNum + 1):
				window = [gameBoard.gameBoard[r + i][c + i].value for i in range(winNum)]
				score += self.scoreWindow(window, me, opp, winNum)

		for r in range(winNum - 1, rows):
			for c in range(cols - winNum + 1):
				window = [gameBoard.gameBoard[r - i][c + i].value for i in range(winNum)]
				score += self.scoreWindow(window, me, opp, winNum)

		return score
	
	def orderedMoves(self, gameBoard, moves):
		center = gameBoard.numColumns // 2
		return sorted(moves, key=lambda c: abs(c - center))
	
	def getMove(self, gameBoard):
		# self.numExpanded = 0
		# self.numPruned = 0

		me = self.name 
		opp = self._opponent()

		MAX_DEPTH = 5

		def minimax(depth, maximizing):
			self.numExpanded += 1
			term = self.terminalValue(gameBoard, me, opp, depth)
			if term is not None:
				return term
			if depth == 0:
				return self._heuristic(gameBoard, me, opp)

			moves = self.orderedMoves(gameBoard, self.legalMoves(gameBoard))
			if not moves:
				return 0 
			if maximizing:
				best = -10**18
				for col in moves:
					gameBoard.addPiece(col, me)
					val = minimax(depth - 1, False)
					gameBoard.removePiece(col)
					if val > best:
						best = val
				return best
			else:
				best = 10**18
				for col in moves:
					gameBoard.addPiece(col, opp)
					val = minimax(depth - 1, True)
					gameBoard.removePiece(col)
					if val < best:
						best = val
				return best
			
		best_move = None
		best_value = -10**18
		for col in self.orderedMoves(gameBoard, self.legalMoves(gameBoard)):
			gameBoard.addPiece(col, me)
			val = minimax(MAX_DEPTH - 1, False)
			gameBoard.removePiece(col)
			if val > best_value:
				best_value = val
				best_move = col
		
		if best_move is None:
			moves = self.orderedMoves(gameBoard, self.legalMoves(gameBoard))
			return moves[0] if moves else 0

		return best_move
	def getMoveAlphaBeta(self, gameBoard):
		# self.numExpanded = 0
		# self.numPruned = 0

		me = self.name
		opp = self._opponent()

		MAX_DEPTH = 7 

		def alphabeta(depth, alpha, beta, maximizing):
			self.numExpanded += 1
			term = self.terminalValue(gameBoard, me, opp, depth)
			if term is not None:
				return term
			if depth == 0:
				return self._heuristic(gameBoard, me, opp)

			moves = self.orderedMoves(gameBoard, self.legalMoves(gameBoard))
			if not moves:
				return 0 
			if maximizing:
				best = -10**18
				for col in moves:
					gameBoard.addPiece(col, me)
					val = alphabeta(depth - 1, alpha, beta, False)
					gameBoard.removePiece(col)
					if val > best:
						best = val
					if best > alpha:
						alpha = best
					if beta <= alpha:
						self.numPruned += 1
						break
				return best
			else:
				best = 10**18
				for col in moves:
					gameBoard.addPiece(col, opp)
					val = alphabeta(depth - 1, alpha, beta, True)
					gameBoard.removePiece(col)
					if val < best:
						best = val
					if best < beta:
						beta = best
					if beta <= alpha:
						self.numPruned += 1
						break
				return best
			
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
				alpha = best_value
		if best_move is None:
			moves = self.orderedMoves(gameBoard, self.legalMoves(gameBoard))
			return moves[0] if moves else 0
		
		return best_move

	