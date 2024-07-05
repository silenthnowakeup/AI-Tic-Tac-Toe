import random
from agent import Agent
from environment import TicTacToe

# Определение количества игр для проверки
NUM_GAMES = 1000


def main():
    # Инициализация игры и агентов
    game = TicTacToe(training=True)
    agent1 = Agent(epsilon=0)
    agent2 = Agent(epsilon=0)

    # Загрузка обученных состояний
    agent1.loadQtable("../states/player1states")
    agent2.loadQtable("../states/player2states")

    # Подсчет результатов
    agent1_wins = 0
    agent2_wins = 0
    draws = 0

    for _ in range(NUM_GAMES):
        game.reset()
        agent1.game_begin()
        agent2.game_begin()
        done = False
        isX = True  # Первым ходит agent1

        while not done:
            if isX:
                move = agent1.epsilon_greedy(game.board, game.possible_moves())
            else:
                move = agent2.epsilon_greedy(game.board, game.possible_moves())

            reward, done = game.step(isX, move)

            if reward == 1:
                if isX:
                    agent1.updateQ(reward, game.board, game.possible_moves())
                    agent2.updateQ(-1 * reward, game.board, game.possible_moves())
                    agent1_wins += 1
                else:
                    agent1.updateQ(-1 * reward, game.board, game.possible_moves())
                    agent2.updateQ(reward, game.board, game.possible_moves())
                    agent2_wins += 1
            elif reward == 0.5:
                agent1.updateQ(reward, game.board, game.possible_moves())
                agent2.updateQ(reward, game.board, game.possible_moves())
                draws += 1

            isX = not isX

    # Вывод результатов
    print(f"Из {NUM_GAMES} игр:")

    print(f"Победы Agent 1: {agent1_wins} ({agent1_wins / NUM_GAMES * 100:.2f}%)")
    print(f"Победы Agent 2: {agent2_wins} ({agent2_wins / NUM_GAMES * 100:.2f}%)")
    print(f"Ничьи: {draws} ({draws / NUM_GAMES * 100:.2f}%)")


if __name__ == "__main__":
    main()
