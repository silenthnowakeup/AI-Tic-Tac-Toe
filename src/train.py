from environment import TicTacToe
from agent import Agent


def main():
    game = TicTacToe(True)  # game instance, True means training
    player1 = Agent()  # player1 learning agent
    player2 = Agent()  # player2 learning agent
    game.train(player1, player2, 200000)
    game.saveStates()  # save Qtable


if __name__ == "__main__":
    main()
