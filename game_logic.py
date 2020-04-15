import random
random.seed()

piece_display = {0: '∙', 1: '■', -1: '□'}
board9 = """
∙(0)--------------------∙(1)--------------------∙(2)
|                       |                       |
|                       |                       |
|                       |                       |
|       ∙(8)------------∙(9)------------∙(10)   |
|       |               |               |       |
|       |               |               |       |
|       |               |               |       |
|       |       ∙(16)---∙(17)---∙(18)   |       |
|       |       |               |       |       |
|       |       |               |       |       |
|       |       |               |       |       |
∙(3)----∙(11)---∙(19)           ∙(20)---∙(12)---∙(4)
|       |       |               |       |       |
|       |       |               |       |       |
|       |       |               |       |       |
|       |       ∙(21)---∙(22)---∙(23)   |       |
|       |               |               |       |
|       |               |               |       |
|       |               |               |       |
|       ∙(13)-----------∙(14)-----------∙(15)   |
|                       |                       |
|                       |                       |
|                       |                       |
∙(5)--------------------∙(6)--------------------∙(7)
"""
board6 = """
∙(0)------------∙(1)------------∙(2)
|               |               |
|               |               |
|               |               |
|       ∙(8)----∙(9)----∙(10)   |
|       |               |       |
|       |               |       |
|       |               |       |
∙(3)----∙(11)           ∙(12)---∙(4)
|       |               |       |
|       |               |       |
|       |               |       |
|       ∙(13)---∙(14)---∙(15)   |
|               |               |
|               |               |
|               |               |
∙(5)------------∙(6)------------∙(7)
"""
board12 = """
∙(0)--------------------∙(1)--------------------∙(2)
| ╲                     |                     ╱ |
|   ╲                   |                   ╱   |
|     ╲                 |                 ╱     |
|       ∙(8)------------∙(9)------------∙(10)   |
|       | ╲             |             ╱ |       |
|       |   ╲           |           ╱   |       |
|       |     ╲         |         ╱     |       |
|       |       ∙(16)---∙(17)---∙(18)   |       |
|       |       |               |       |       |
|       |       |               |       |       |
|       |       |               |       |       |
∙(3)----∙(11)---∙(19)           ∙(20)---∙(12)---∙(4)
|       |       |               |       |       |
|       |       |               |       |       |
|       |       |               |       |       |
|       |       ∙(21)---∙(22)---∙(23)   |       |
|       |     ╱         |         ╲     |       |
|       |   ╱           |           ╲   |       |
|       | ╱             |             ╲ |       |
|       ∙(13)-----------∙(14)-----------∙(15)   |
|     ╱                 |                 ╲     |
|   ╱                   |                   ╲   |
| ╱                     |                     ╲ |
∙(5)--------------------∙(6)--------------------∙(7)
"""

class morris_game:
	"""
	Tracks current board position, which player's turn, and history of moves
	"""
	def __init__(self, n_pieces, board=None, color=1, turns_played=0, move_desc='Game start!'):
		"""
		:param n_pieces: number of pieces per player, determines the type of game.
			9 for Nine Men's Morris, 6 for Six Men's Morris
		:param board: list of integers that defines the board layout. The items in
			the list are the positions on the board: 0 means empty, 1 means white
			piece, -1 means black piece
		:param color: which player has the current turn: 1 (white) or -1 (black)
		:param turns_played: integer, initially 0
		:param move_desc: description of most recent move
		"""
		self.n_pieces = n_pieces
		try:
			board_length = {9: 24, 6: 16, 12: 24}[self.n_pieces]
		except:
			raise ValueError(f'Unknown game type with {n_pieces} pieces')

		if board is None:
			self.board = [0] * board_length
		else:
			if len(board) != board_length:
				raise ValueError(f'Input board length does not match expected length {board_length}')
			self.board = board.copy()
		self.color = color
		self.turns_played = turns_played
		self.move_desc = move_desc

	def copy(self):
		"""
		Clone of game that can be edited without affecting original
		"""
		return morris_game(self.n_pieces, self.board, self.color, self.turns_played, self.move_desc)

	def invert(self):
		"""
		Return a clone of game with players inverted

		This is for heuristic calculations; equivalent to inverting the board
		"""
		return morris_game(self.n_pieces, self.board, -self.color, self.turns_played, self.move_desc)

	def count(self):
		"""
		Number of pieces on the board for current player
		"""
		return self.board.count(self.color)

	def stage(self):
		"""
		Which stage of the game the current player is in
		"""
		if self.turns_played < self.n_pieces * 2:
			return 1
		elif self.count() > 3:
			return 2
		else:
			return 3

	def print(self):
		"""
		Output ascii layout of current board and most recent move
		"""
		board_disp = {9: board9, 6: board6, 12: board12}[self.n_pieces]
		for pos, color in enumerate(self.board):
			board_disp = board_disp.replace(f'∙({pos})', f'{piece_display[color]}({pos})')
		print(board_disp, '\n', self.move_desc)

	def adjacents(self, pos):
		"""
		Return list of adjacent positions to input position
		"""
		adjacent = {9: [
			[1, 3],
			[0, 2, 9],
			[1, 4],
			[0, 5, 11],
			[2, 7, 12],
			[3, 6],
			[5, 7, 14],
			[4, 6],
			[9, 11],
			[1, 8, 10, 17],
			[9, 12],
			[3, 8, 13, 19],
			[4, 10, 15, 20],
			[11, 14],
			[6, 13, 15, 22],
			[12, 14],
			[17, 19],
			[9, 16, 18],
			[17, 20],
			[11, 16, 21],
			[12, 18, 23],
			[19, 22],
			[21, 23, 14],
			[20, 22]
		], 6: [
			[1, 3],
			[0, 2, 9],
			[1, 4],
			[0, 5, 11],
			[2, 7, 12],
			[3, 6],
			[5, 7, 14],
			[4, 6],
			[9, 11],
			[1, 8, 10],
			[9, 12],
			[3, 8, 13],
			[4, 10, 15],
			[11, 14],
			[6, 13, 15],
			[12, 14]
		], 12: [
            [1, 3, 8],
            [0, 2, 9],
            [1, 4, 10],
            [0, 5, 11],
            [2, 7, 12],
            [3, 6, 13],
            [5, 7, 14],
            [4, 6, 15],
            [0, 9, 11, 16],
            [1, 8, 10, 17],
            [2, 9, 12, 18],
            [3, 8, 13, 19],
            [4, 10, 15, 20],
            [5, 11, 14, 21],
            [6, 13, 15, 22],
            [7, 12, 14, 23],
            [8, 17, 19],
            [9, 16, 18],
            [10, 17, 20],
            [11, 16, 21],
            [12, 18, 23],
            [13, 19, 22],
            [21, 23, 14],
            [15, 20, 22]
		]}
		return adjacent[self.n_pieces][pos]

	def checkMillFormation(self, pos, color):
		"""
		Check whether a mill would be formed if piece of specified color placed at
		the specified position
		"""
		mill = {9: [
			[[1, 2], [3, 5]],
			[[0, 2], [9, 17]],
			[[0, 1], [4, 7]],
			[[0, 5], [11, 19]],
			[[2, 7], [12, 20]],
			[[0, 3], [6, 7]],
			[[5, 7], [14, 22]],
			[[2, 4], [5, 6]],
			[[9, 10], [11, 13]],
			[[8, 10], [1, 17]],
			[[8, 9], [12, 15]],
			[[3, 19], [8, 13]],
			[[20, 4], [10, 15]],
			[[8, 11], [14, 15]],
			[[13, 15], [6, 22]],
			[[13, 14], [10, 12]],
			[[17, 18], [19, 21]],
			[[1, 9], [16, 18]],
			[[16, 17], [20, 23]],
			[[16, 21], [3, 11]],
			[[12, 4], [18, 23]],
			[[16, 19], [22, 23]],
			[[6, 14], [21, 23]],
			[[18, 20], [21, 22]]
		], 6: [
			[[1, 2], [3, 5]],
			[[0, 2]],
			[[0, 1], [4, 7]],
			[[0, 5]],
			[[2, 7]],
			[[0, 3], [6, 7]],
			[[5, 7]],
			[[2, 4], [5, 6]],
			[[9, 10], [11, 13]],
			[[8, 10]],
			[[8, 9], [12, 15]],
			[[8, 13]],
			[[10, 15]],
			[[8, 11], [14, 15]],
			[[13, 15]],
			[[13, 14], [10, 12]]
		], 12: [
            [[1, 2], [3, 5], [8, 16]],
            [[0, 2], [9, 17]],
            [[0, 1], [4, 7], [10, 18]],
            [[0, 5], [11, 19]],
            [[2, 7], [12, 20]],
            [[0, 3], [6, 7], [13, 21]],
            [[5, 7], [14, 22]],
            [[2, 4], [5, 6], [15, 23]],
            [[9, 10], [11, 13], [0, 16]],
            [[8, 10], [1, 17]],
            [[8, 9], [12, 15], [2, 18]],
            [[3, 19], [8, 13]],
            [[20, 4], [10, 15]],
            [[8, 11], [14, 15], [5, 21]],
            [[13, 15], [6, 22]],
            [[13, 14], [10, 12], [7, 23]],
            [[17, 18], [19, 21], [0, 8]],
            [[1, 9], [16, 18]],
            [[16, 17], [20, 23], [2, 10]],
            [[16, 21], [3, 11]],
            [[12, 4], [18, 23]],
            [[16, 19], [22, 23], [5, 13]],
            [[6, 14], [21, 23]],
            [[18, 20], [21, 22], [7, 15]]
		]}
		pos_pairs = mill[self.n_pieces][pos]
		return any([self.board[pos1] == color and self.board[pos2] == color for pos1, pos2 in pos_pairs])

	def isCloseMill(self, pos):
		"""
		Check whether specified position forms a part of an existing mill
		"""
		color = self.board[pos]
		return self.checkMillFormation(pos, color) if color else False

	def advance_game(self, move_desc):
		"""
		Advance game by one turn

		Does not change the board layout - that needs to be done separately
		"""
		self.color = -self.color
		self.turns_played += 1
		self.move_desc = move_desc

	def moves(self):
		"""
		List of all possible next moves for current player, in random order

		:returns: list of games whose boards and move_desc have been updated
		"""
		game_list = []
		stage = self.stage()
		if stage == 1:
			empty_list = [pos for pos, piece in enumerate(self.board) if not piece]
			random.shuffle(empty_list)
			for pos in empty_list:
				game_clone = self.copy()
				game_clone.board[pos] = self.color
				game_clone.advance_game(f'{piece_display[self.color]} placed at {pos}')
				if game_clone.isCloseMill(pos): # if mill is formed, complete the move by removing opponent's piece
					# move these moves to the top of the list (speeds up alpha-beta pruning)
					game_list = game_clone.remove_moves() + game_list
				else:
					game_list.append(game_clone)
		else:
			pos1_list = [pos for pos, piece in enumerate(self.board) if piece == self.color]
			random.shuffle(pos1_list)
			for pos1 in pos1_list:
				pos2_list = self.adjacents(pos1) if stage == 2 else range(len(self.board))
				pos2_list = [pos for pos in pos2_list if not self.board[pos]]
				random.shuffle(pos2_list)
				for pos2 in pos2_list:
					game_clone = self.copy()
					game_clone.board[pos1] = 0
					game_clone.board[pos2] = self.color
					game_clone.advance_game(f'{piece_display[self.color]} moved from {pos1} to {pos2}')
					if game_clone.isCloseMill(pos2): # if mill is formed, complete the move by removing opponent's piece
						# move these moves to the top of the list (speeds up alpha-beta pruning)
						game_list = game_clone.remove_moves() + game_list
					else:
						game_list.append(game_clone)
		return game_list

	def remove_moves(self):
		"""
		List of complete moves in which one piece of current player is removed, in random order

		Function advance_game() should have already been run. Appends to most recent move description.
	
		:returns: list of games with moves completed
		"""
		game_list = []
		# piece can be removed if position has right player's piece and is not part of an existing mill, unless there are 3 pieces left
		rem_list = [pos for pos, piece in enumerate(self.board) if piece == self.color and (not self.isCloseMill(pos) or self.count() == 3)]
		random.shuffle(rem_list)
		for pos in rem_list:
			game_clone = self.copy()
			game_clone.board[pos] = 0
			game_clone.move_desc += f' and {piece_display[self.color]} removed from {pos}'
			game_list.append(game_clone)
		return game_list

	def human_move(self):
		"""
		Get human input for current player's move and advance game
		"""
		stage = self.stage()
		if stage == 1:
			while True:
				try:
					pos = int(input(f"Place {piece_display[self.color]} piece: "))
					piece_at_pos = self.board[pos]
				except Exception:
					print("Invalid input")
					continue
				if piece_at_pos != 0:
					print("There is already a piece there")
					continue
				break
			self.board[pos] = self.color
			self.advance_game(f'{piece_display[self.color]} placed at {pos}')
			if self.isCloseMill(pos):
				self.human_remove()
		else:
			while True:
				try:
					pos1 = int(input(f"Move {piece_display[self.color]} piece: "))
					piece_at_pos1 = self.board[pos1]
				except Exception:
					print("Invalid input")
					continue
				if piece_at_pos1 != self.color:
					print(f"There is no {piece_display[self.color]} piece there")
					continue
				if stage == 2 and [self.board[p] for p in self.adjacents(pos1)].count(0) == 0:
					print("That piece has no adjacent positions available")
					continue
				break
			self.board[pos1] = 0
			while True:
				try:
					pos2 = int(input(f"New location for {piece_display[self.color]}: "))
					piece_at_pos2 = self.board[pos2]
				except Exception:
					print("Invalid input")
					continue
				if piece_at_pos2 != 0:
					print("There is already a piece there")
					continue
				if stage == 2 and pos2 not in self.adjacents(pos1):
					print("That position is not next to the piece")
					continue
				break
			self.board[pos2] = self.color
			self.advance_game(f'{piece_display[self.color]} moved from {pos1} to {pos2}')
			if self.isCloseMill(pos2):
				self.human_remove()

	def human_remove(self):
		"""
		Get human input to remove a piece as part of a move

		At this point self.color is the type of piece to remove
		"""
		while True:
			try:
				pos = int(input(f"Remove {piece_display[self.color]} piece: "))
				piece_at_pos = self.board[pos]
			except Exception:
				print("Invalid input")
				continue
			if piece_at_pos != self.color:
				print(f"There is no {piece_display[self.color]} piece there")
				continue
			if self.isCloseMill(pos) and self.count() > 3:
				print("That piece is part of a mill and cannot be removed")
				continue
			break
		self.board[pos] = 0
		self.move_desc += f' and {piece_display[self.color]} removed from {pos}'

	def check_end(self):
		"""
		Check whether game is in end state

		:returns: game end message, else 0
		"""
		if self.stage() == 1:
			return 0
		else:
			if self.board.count(-self.color) <= 2:
				# shouldn't happen if we're checking every turn
				return f'Player {piece_display[self.color]} wins!'
			elif self.count() <= 2:
				return f'Player {piece_display[-self.color]} wins!'
			player_moves = len(self.moves())
			opponent_moves = len(self.invert().moves())
			if player_moves == 0 and opponent_moves == 0:
				return 'Game ends in stalemate' # This can happen in twelve men's morris
			elif player_moves == 0:
				return f'Player {piece_display[-self.color]} wins!' # Opponent wins
			else:
				return 0
