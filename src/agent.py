# agent.py

import random
import pickle


class Agent:
    def __init__(self, epsilon=0.1, alpha=0.1, gamma=0.9):
        """
        Инициализация агента с параметрами epsilon, alpha, gamma для Q-обучения.

        Args:
        - epsilon (float): Вероятность случайного действия при выборе в стратегии ε-greedy.
        - alpha (float): Learning rate для обновления Q-значений.
        - gamma (float): Discount factor для будущих наград.

        Attributes:
        - Q (dict): Q-таблица для хранения оценок состояний-действий.
        - last_board (tuple): Последнее состояние игрового поля.
        - q_last (float): Последнее оцененное Q-значение для последнего действия.
        - state_action_last (tuple): Последнее состояние-действие.

        """
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.Q = {}  # Q таблица
        self.last_board = None
        self.q_last = 0.0
        self.state_action_last = None
        self.role = role
    def switch_role(self):
        self.role = 'O' if self.role == 'X' else 'X'

    def game_begin(self):
        """
        Сброс состояния агента перед началом новой игры.
        """
        self.last_board = None
        self.q_last = 0.0
        self.state_action_last = None

    def epslion_greedy(self, state, possible_moves):
        """
        Выбор действия по стратегии ε-greedy.

        Args:
        - state (list): Текущее состояние игрового поля.
        - possible_moves (list): Список возможных действий (ходов).

        Returns:
        - move: Выбранное действие.

        """
        self.last_board = tuple(state)
        if random.random() < self.epsilon:
            move = random.choice(possible_moves)  # Случайное действие
            self.state_action_last = (self.last_board, move)
            self.q_last = self.getQ(self.last_board, move)
            return move
        else:
            # Greedy strategy
            Q_list = [self.getQ(self.last_board, action) for action in possible_moves]
            maxQ = max(Q_list)

            if Q_list.count(maxQ) > 1:
                # Более одного лучшего варианта; выбираем случайным образом
                best_options = [i for i in range(len(possible_moves)) if Q_list[i] == maxQ]
                i = random.choice(best_options)
            else:
                i = Q_list.index(maxQ)

            self.state_action_last = (self.last_board, possible_moves[i])
            self.q_last = self.getQ(self.last_board, possible_moves[i])
            return possible_moves[i]

    def getQ(self, state, action):
        """
        Получение Q-значения для данного состояния и действия.

        Args:
        - state (tuple): Состояние игрового поля.
        - action: Действие (ход).

        Returns:
        - float: Значение Q-функции для пары (state, action).

        """
        if (state, action) not in self.Q:
            self.Q[(state, action)] = 1.0  # Инициализация Q-значения
        return self.Q[(state, action)]

    def updateQ(self, reward, state, possible_moves):
        """
        Обновление Q-значения по алгоритму Q-обучения.

        Args:
        - reward (float): Награда за последнее совершенное действие.
        - state (list): Текущее состояние игрового поля.
        - possible_moves (list): Список возможных действий (ходов).

        """
        q_list = [self.getQ(tuple(state), move) for move in possible_moves]
        max_q_next = max(q_list) if q_list else 0.0

        self.Q[self.state_action_last] = self.q_last + self.alpha * ((reward + self.gamma * max_q_next) - self.q_last)

    def saveQtable(self, file_name):
        """
        Сохранение Q-таблицы в файл.

        Args:
        - file_name (str): Имя файла для сохранения.

        """
        with open(file_name, 'wb') as handle:
            pickle.dump(self.Q, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def loadQtable(self, file_name):
        """
        Загрузка Q-таблицы из файла.

        Args:
        - file_name (str): Имя файла для загрузки.

        """
        with open(file_name, 'rb') as handle:
            self.Q = pickle.load(handle)
