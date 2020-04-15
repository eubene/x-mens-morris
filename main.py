import game_logic
import ai

game_select = """
================================
NINE MEN'S MORRIS (and variants)
================================

Which game do you want to play?
[6]  Six Men's Morris
[9]  Nine Men's Morris (default)
[12] Twelve Men's Morris
: """

player_select = """
Select players for white/black
      ■        □
[A] Human    Human
[B] Human     AI    (default)
[C]  AI      Human
[D]  AI       AI
[E] Manually select each turn
: """
d_player_select = {
	'A': ('human', 'human'),
	'B': ('human', 'ai'),
	'C': ('ai', 'human'),
	'D': ('ai', 'ai'),
	'E': ('manual', 'manual')
}

def main():
	# Select game
	try:
		n_pieces = int(input(game_select))
	except Exception:
		n_pieces = 9
	except KeyboardInterrupt:
		print('\nQuit')
		return
	game = game_logic.morris_game(n_pieces)

	# Select players
	try:
		player_types = d_player_select[input(player_select).upper()]
	except Exception:
		player_types = ('human', 'ai')
	except KeyboardInterrupt:
		print('\nQuit')
		return

	# Play game
	while True:
		game.print()

		# Check for game end
		msg = game.check_end()
		if msg:
			print(msg)
			break

		# Play a turn
		player_type = player_types[{1: 0, -1: 1}[game.color]]
		if player_type == 'manual':
			try:
				if input('Enter [H] for human: ').upper() == 'H':
					player_type = 'human'
				else:
					player_type = 'ai'
			except Exception:
				player_type = 'ai'
			except KeyboardInterrupt:
				print('\nQuit')
				return
		if player_type == 'human':
			try:
				game.human_move()
			except KeyboardInterrupt:
				print('\nQuit')
				return
		else: # player_type == 'ai'
			print('AI plays turn')
			game = ai.alphabeta(game, 5)

if __name__ == "__main__":
	main()
