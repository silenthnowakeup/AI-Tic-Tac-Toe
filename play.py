from environment import TicTacToe, Human
from agent import Agent

game = TicTacToe()  # game instance
player1 = Human()  # human player
player2 = Agent()  # agent
game.startGame(player1, player2)  # player1 is X, player2 is 0
game.reset()  # reset
