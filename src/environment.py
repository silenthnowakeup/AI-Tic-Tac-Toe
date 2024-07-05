import pygame
import random
import time
from agent import Agent
import matplotlib.pyplot as plt

# Human player
class Human:
    pass


# Random player
class Randomplayer:
    def __init__(self):
        pass

    def move(self, possiblemoves):
        """
        Выбор случайного действия из списка возможных ходов.

        Args:
        - possiblemoves (list): Список возможных ходов.

        Returns:
        - move: Выбранный случайный ход.
        """
        return random.choice(possiblemoves)


# TicTacToe game
class TicTacToe:
    def __init__(self, training=False):
        """
        Инициализация игры "крестики-нолики".

        Args:
        - training (bool): Режим обучения (по умолчанию False).
        """
        self.board = [' '] * 9  # Игровое поле
        self.done = False  # Флаг завершения игры
        self.human = None  # Человеческий игрок
        self.computer = None  # Компьютерный игрок
        self.humanTurn = True  # Признак очереди хода человека
        self.training = training  # Режим обучения
        self.player1 = None  # Игрок 1
        self.player2 = None  # Игрок 2
        self.ai = None  # Искусственный интеллект
        self.isAI = False  # Флаг, указывающий на использование AI

        if not training:
            pygame.init()
            # Настройки графического интерфейса
            self.WIDTH, self.HEIGHT = 500, 500
            self.BOARD_ROWS = 3
            self.BOARD_COLS = 3
            self.LINE_WIDTH = 15
            self.SQUARE_SIZE = self.WIDTH // self.BOARD_COLS
            self.CIRCLE_RADIUS = self.SQUARE_SIZE // 3
            self.CIRCLE_WIDTH = 15
            self.CROSS_WIDTH = 25
            self.SPACE = self.SQUARE_SIZE // 4
            self.CIRCLE_COLOR = (239, 231, 200)
            self.CROSS_COLOR = (66, 66, 66)
            self.TEXT_COLOR = (66, 66, 66)
            self.BG_COLOR = (28, 170, 156)
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
            self.screen.fill(self.BG_COLOR)
            self.LINE_COLOR = (23, 145, 135)

            pygame.display.set_caption('Tic Tac Toe')
            self.font = pygame.font.Font(None, 74)

    def reset(self):
        """
        Сброс игрового поля до начального состояния.
        """
        self.board = [' '] * 9
        self.done = False
        self.humanTurn = True
        if not self.training:
            self.screen.fill(self.BG_COLOR)
            self.draw_lines()
            pygame.display.update()

    def draw_lines(self):
        """
        Отрисовка линий игрового поля.
        """
        # Горизонтальные линии
        for row in range(1, self.BOARD_ROWS):
            pygame.draw.line(self.screen, self.LINE_COLOR, (0, row * self.SQUARE_SIZE),
                             (self.WIDTH, row * self.SQUARE_SIZE), self.LINE_WIDTH)
        # Вертикальные линии
        for col in range(1, self.BOARD_COLS):
            pygame.draw.line(self.screen, self.LINE_COLOR, (col * self.SQUARE_SIZE, 0),
                             (col * self.SQUARE_SIZE, self.HEIGHT), self.LINE_WIDTH)

    def draw_figures(self):
        """
        Отрисовка фигур (крестиков и ноликов) на игровом поле.
        """
        for i in range(9):
            row = i // 3
            col = i % 3
            if self.board[i] == 'X':
                pygame.draw.line(self.screen, self.CROSS_COLOR,
                                 (col * self.SQUARE_SIZE + self.SPACE,
                                  row * self.SQUARE_SIZE + self.SQUARE_SIZE - self.SPACE),
                                 (col * self.SQUARE_SIZE + self.SQUARE_SIZE - self.SPACE,
                                  row * self.SQUARE_SIZE + self.SPACE), self.CROSS_WIDTH)
                pygame.draw.line(self.screen, self.CROSS_COLOR,
                                 (col * self.SQUARE_SIZE + self.SPACE, row * self.SQUARE_SIZE + self.SPACE),
                                 (col * self.SQUARE_SIZE + self.SQUARE_SIZE - self.SPACE,
                                  row * self.SQUARE_SIZE + self.SQUARE_SIZE - self.SPACE),
                                 self.CROSS_WIDTH)
            elif self.board[i] == 'O':
                pygame.draw.circle(self.screen, self.CIRCLE_COLOR,
                                   (int(col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2),
                                    int(row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2)),
                                   self.CIRCLE_RADIUS, self.CIRCLE_WIDTH)

    def display_end_game(self, result):
        """
        Отображение сообщения о завершении игры.

         Args:
            - result (str): Сообщение о результате игры.
        """

        self.screen.fill(self.BG_COLOR)
        if result == "x_win":
            text = self.font.render("ПОБЕДИТЕЛЬ!", True, self.TEXT_COLOR)
            self.screen.blit(text, (self.WIDTH // 4 - 65, self.HEIGHT // 2 - 125))
            pygame.draw.line(self.screen, self.CROSS_COLOR, (self.WIDTH // 2 - 50, self.HEIGHT // 2 - 50),
                             (self.WIDTH // 2 + 50, self.HEIGHT // 2 + 50), self.CROSS_WIDTH)
            pygame.draw.line(self.screen, self.CROSS_COLOR, (self.WIDTH // 2 - 50, self.HEIGHT // 2 + 50),
                             (self.WIDTH // 2 + 50, self.HEIGHT // 2 - 50), self.CROSS_WIDTH)
        elif result == "o_win":
            text = self.font.render("ПОБЕДИТЕЛЬ!", True, self.TEXT_COLOR)
            self.screen.blit(text, (self.WIDTH // 4 - 65, self.HEIGHT // 2 - 125))
            pygame.draw.circle(self.screen, self.CIRCLE_COLOR, (self.WIDTH // 2, self.HEIGHT // 2), 50,
                               self.CIRCLE_WIDTH)
        elif result == "draw":
            text = self.font.render("НИЧЬЯ!", True, self.TEXT_COLOR)
            self.screen.blit(text, (self.WIDTH // 3 - 10, self.HEIGHT // 2 - 125))
        pygame.display.update()

    def startGame(self, playerX, playerO):
        """
        Начало игры между двумя игроками.

         Args:
        - playerX: Игрок, играющий за X.
        - playerO: Игрок, играющий за O.
        """
        self.human = True if isinstance(playerX, Human) else False
        self.computer = True if isinstance(playerO, Human) else False
        self.humanTurn = True  # Ensure human goes first

        if isinstance(playerO, Agent):
            self.ai = playerO
            self.ai.loadQtable("../states/player2states")
            self.ai.epsilon = 0
            self.isAI = True
        elif isinstance(playerO, Randomplayer):
            self.ai = playerO
            self.isAI = False

        self.reset()
        self.play_game()

    def play_game(self):
        """
        Основной цикл игры, обработка ходов и отображение результатов.
        """
        running = True
        while running:
            if self.humanTurn:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = self.get_click_position()
                        if pos is not None and self.board[pos] == ' ':
                            self.board[pos] = 'X'
                            self.humanTurn = False
                            self.draw_figures()
                            reward, done = self.evaluate('X')
                            if done:
                                self.display_end_game("x_win" if reward == 1.0 else "draw")
                                time.sleep(1)
                                self.reset()
            else:
                if self.isAI:
                    move = self.ai.epsilon_greedy(self.board, self.possible_moves())
                else:
                    move = self.ai.move(self.possible_moves())
                if move is not None:
                    self.board[move - 1] = 'O'
                    self.humanTurn = True
                    self.draw_figures()
                    reward, done = self.evaluate('O')
                    if done:
                        self.display_end_game("o_win" if reward == 1.0 else "draw")
                        time.sleep(1)
                        self.reset()
            pygame.display.update()

    def get_click_position(self):
        x, y = pygame.mouse.get_pos()
        col = x // self.SQUARE_SIZE
        row = y // self.SQUARE_SIZE
        return row * 3 + col if self.board[row * 3 + col] == ' ' else None

    def evaluate(self, ch):
        """
        Оценка текущего состояния игры (победа, ничья, продолжение игры).

         Args:
            - ch: Игрок, делающий ход

         Returns:
            - bool: True, если игра завершена, иначе False.
        """
        # Rows checking
        for i in range(3):
            if ch == self.board[i * 3] == self.board[i * 3 + 1] == self.board[i * 3 + 2]:
                return 1.0, True
        # Columns checking
        for i in range(3):
            if ch == self.board[i] == self.board[i + 3] == self.board[i + 6]:
                return 1.0, True
        # Diagonals checking
        if ch == self.board[0] == self.board[4] == self.board[8]:
            return 1.0, True
        if ch == self.board[2] == self.board[4] == self.board[6]:
            return 1.0, True
        # Check for draw
        if ' ' not in self.board:
            return 0.5, True

        return 0.0, False

    def possible_moves(self):
        """
        Возвращает список доступных ходов.

         Returns:
            - list: Список индексов доступных клеток.
        """

        return [i + 1 for i, v in enumerate(self.board) if v == ' ']

    def drawMove(self, pos, isX):
        """
        Отображение хода на игровом поле.
         Args:
            - pos (int): Индекс клетки для хода.
            - isX (str): Игрок ('X' или 'O').

         """
        self.board[pos - 1] = 'X' if isX else 'O'
        self.draw_figures()
        reward, done = self.evaluate('X' if isX else 'O')
        return reward, done

    def train(self, player1, player2, iterations, epsilon_decay=0.9):
        """
        Функция обучения агента.
        Args:
            - iterations (int): Количество итераций.

         """
        if isinstance(player1, Agent) and isinstance(player2, Agent):
            self.training = True
            self.player1 = player1
            self.player2 = player2
        if self.training:
            for i in range(iterations):
                print(f"training", i)
                self.player1.game_begin()
                self.player2.game_begin()
                self.reset()
                done = False
                isX = random.choice([True, False])
                while not done:
                    if isX:
                        move = self.player1.epsilon_greedy(self.board, self.possible_moves())
                    else:
                        move = self.player2.epsilon_greedy(self.board, self.possible_moves())

                    reward, done = self.step(isX, move)

                    if reward == 1:
                        if isX:
                            self.player1.updateQ(reward, self.board, self.possible_moves())
                            self.player2.updateQ(-1 * reward, self.board, self.possible_moves())
                        else:
                            self.player1.updateQ(-1 * reward, self.board, self.possible_moves())
                            self.player2.updateQ(reward, self.board, self.possible_moves())

                    elif reward == 0.5:
                        self.player1.updateQ(reward, self.board, self.possible_moves())
                        self.player2.updateQ(reward, self.board, self.possible_moves())

                    elif reward == -5:
                        if isX:
                            self.player1.updateQ(reward, self.board, self.possible_moves())
                        else:
                            self.player2.updateQ(reward, self.board, self.possible_moves())

                    elif reward == 0:
                        if isX:
                            self.player2.updateQ(reward, self.board, self.possible_moves())
                        else:
                            self.player1.updateQ(reward, self.board, self.possible_moves())
                    isX = not isX
                player1.epsilon *= epsilon_decay
                player2.epsilon *= epsilon_decay


    def saveStates(self):
        """
        Сохранение Q-таблиц.
        """
        self.player1.saveQtable("../states/player1states")
        self.player2.saveQtable("../states/player2states")

    # Take next step and return reward
    def step(self, isX, move):
        """
        Делает шаг в нашем среде
        Args:
            - isX (bool): Игрок ('X' или 'O').
            - move (int): Ход.
        Returns:
            - reward (float): Результат хода.
            - done (bool): Завершена ли игра.
        """
        ch = 'X' if isX else 'O'
        if self.board[move - 1] != ' ':
            return -5, True

        self.board[move - 1] = ch
        reward, done = self.evaluate(ch)
        return reward, done