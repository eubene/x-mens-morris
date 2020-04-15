def alphabeta(game, depth, alpha=-10000, beta=10000, color=None):
	"""
	Recursively run minimax algorithm with alpha-beta pruning

	https://en.wikipedia.org/wiki/Alpha–beta_pruning

	:param game: game state node in the game tree
	:param depth: recursively decreases to zero from initial positive integer
	:param alpha: as described in the alpha-beta algorithm
	:param beta: as described in the alpha-beta algorithm
	:param color: which player is the maximizing player
	:returns: initial call returns optimal move, otherwise optimal score
	"""
	initial_call = True if color is None else False
	if initial_call: color = game.color # current player is maximizing player

	if depth == 0 or game.check_end():
		return HybridHeuristic(game)
	if color == 1:
		score = -10000
		for move in game.moves():
			child_score = alphabeta(move, depth - 1, alpha, beta, -1)
			#print(f'{depth} {child_score:6d} {score:6d} {alpha:6d} {beta:6d} "{move.move_desc}"')
			if child_score >= score:
				score = child_score
				optimal_move = move
			alpha = max(alpha, score)
			if alpha >= beta:
				break
		return optimal_move if initial_call else score
	else: # color == -1
		score = 10000
		for move in game.moves():
			child_score = alphabeta(move, depth - 1, alpha, beta, 1)
			#print(f'{depth} {child_score:6d} {score:6d} {alpha:6d} {beta:6d} "{move.move_desc}"')
			if child_score <= score:
				score = child_score
				optimal_move = move
			beta = min(beta, score)
			if alpha >= beta:
				break
		return optimal_move if initial_call else score

def numberOfPiecesHeuristic(game):
	'''
	Heuristic that looks at the number of pieces on the board
	'''
	game.color = 1
	player_tokens = game.count()
	opponent_tokens = game.board.count(-game.color)
	if game.stage() == 1:
		return 100 * player_tokens - 100 * opponent_tokens
	elif player_tokens <= 2 or len(game.moves()) == 0:
		return -10000
	elif opponent_tokens <= 2 or len(game.invert().moves()) == 0:
		return 10000
	else:
		return 200 * player_tokens - 200 * opponent_tokens

def getPossibleMillCount(game):
	"""
	Count number of mills that can be formed by adding a piece to an empty position
	"""
	return sum([game.checkMillFormation(pos, game.color) for pos, piece in enumerate(game.board) if not piece])

def getPiecesInPotentialMillFormation(game):
	"""
	Count number of mills that would be formed if an opponent's piece were replaced by current player's piece
	"""
	return sum([game.checkMillFormation(pos, game.color) for pos, piece in enumerate(game.board) if piece == -game.color])

def potentialMillsHeuristic(game):
	'''
	Heuristic that looks at the number of potential mills on the board
	'''
	game.color = 1
	player_tokens = game.count()
	opponent_tokens = game.board.count(-game.color)
	if game.stage() > 1 and (player_tokens <= 2 or len(game.moves()) == 0):
		return -10000
	elif game.stage() > 1 and (opponent_tokens <= 2 or len(game.invert().moves()) == 0):
		return 10000
	possible_mills = getPossibleMillCount(game)
	potential_mills = getPiecesInPotentialMillFormation(game)
	if (player_tokens <= 3):
		return 100 * possible_mills + 200 * potential_mills
	else:
		return 200 * possible_mills + 100 * potential_mills

def numberOfMoveablePiecesHeuristic(game):
	'''
	Heuristic that looks at the number of pieces and if they can move
	'''
	game.color = 1
	player_tokens = game.count()
	opponent_tokens = game.board.count(-game.color)
	moveable_pieces = len(game.moves())
	if game.stage() > 1 and (player_tokens <= 2 or moveable_pieces == 0):
		return -10000
	elif game.stage() > 1 and (opponent_tokens <= 2 or len(game.invert().moves()) == 0):
		return 10000
	return 100 * player_tokens - 100 * opponent_tokens - 50 * moveable_pieces

def AdvancedHeuristic(game):
	'''
	Heuristic that looks at the number of pieces and the potential mills
	 that could be formed
	'''
	game.color = 1
	player_tokens = game.count()
	opponent_tokens = game.board.count(-game.color)
	moveable_pieces = len(game.moves())
	if game.stage() > 1 and (player_tokens <= 2 or moveable_pieces == 0):
		return -10000
	elif game.stage() > 1 and (opponent_tokens <= 2 or len(game.invert().moves()) == 0):
		return 10000
	score = 0
	possible_mills = getPossibleMillCount(game)
	potential_mills = getPiecesInPotentialMillFormation(game)
	if player_tokens <= 3:
		score += 100 * possible_mills
		score += 200 * potential_mills
	else:
		score += 200 * possible_mills
		score += 100 * potential_mills
	score -= 25 * moveable_pieces
	score += 50 * (player_tokens - opponent_tokens)
	return score

def HybridHeuristic(game):
	"""
	Use number-of-pieces heuristic if stage 1, and advanced heuristic otherwise

	This is basically what Indronil Prince used
	"""
	game.color = 1
	player_tokens = game.count()
	opponent_tokens = game.board.count(-game.color)
	moveable_pieces = len(game.moves())
	if game.stage() == 1:
		return 100 * player_tokens - 100 * opponent_tokens
	elif game.stage() > 1 and (player_tokens <= 2 or moveable_pieces == 0):
		return -10000
	elif game.stage() > 1 and (opponent_tokens <= 2 or len(game.invert().moves()) == 0):
		return 10000
	# else
	score = 0
	possible_mills = getPossibleMillCount(game)
	potential_mills = getPiecesInPotentialMillFormation(game)
	if player_tokens <= 3:
		score += 100 * possible_mills
		score += 200 * potential_mills
	else:
		score += 200 * possible_mills
		score += 100 * potential_mills
	score -= 25 * moveable_pieces
	score += 50 * (player_tokens - opponent_tokens)
	return score
