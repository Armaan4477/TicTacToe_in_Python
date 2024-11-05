from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton
from PyQt6.QtCore import QTimer
import random

class GameScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_player = "X"
        self.board = [""] * 9
        self.player1_name = ""
        self.player2_name = ""
        self.player1_score = 0
        self.player2_score = 0
        self.is_one_player_mode = False
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.score_label = QLabel()
        self.score_label.setStyleSheet("font-size: 18px; color: black;")
        layout.addWidget(self.score_label)

        grid_layout = QGridLayout()
        self.buttons = []

        for i in range(9):
            button = QPushButton()
            button.setFixedSize(80, 80)
            button.setStyleSheet("font-size: 24px; background-color: #f0f0f0; border: 1px solid #a0a0a0; border-radius: 5px;")
            button.clicked.connect(self.make_move(i))
            self.buttons.append(button)
            grid_layout.addWidget(button, i // 3, i % 3)

        layout.addLayout(grid_layout)

        end_button = QPushButton("End Game")
        end_button.setStyleSheet("font-size: 18px; padding: 10px; color: black; background-color: #a0a0a0; border: 1px solid #707070; border-radius: 5px;")
        end_button.clicked.connect(self.main_window.show_final_scores_screen)
        layout.addWidget(end_button)

        self.setLayout(layout)

    def update_score_label(self):
        self.score_label.setText(f"{self.player1_name} (X): {self.player1_score}\n{self.player2_name} (O): {self.player2_score}")

    def make_move(self, index):
        def callback():
            if self.board[index] == "" and not self.check_winner():
                self.board[index] = self.current_player
                self.buttons[index].setText(self.current_player)
                self.buttons[index].setEnabled(False)
                if self.current_player == "X":
                    self.buttons[index].setStyleSheet("font-size: 24px; background-color: red; color: black; border-radius: 5px;")
                else:
                    self.buttons[index].setStyleSheet("font-size: 24px; background-color: blue; color: black; border-radius: 5px;")
                if self.check_winner():
                    if self.current_player == "X":
                        self.player1_score += 1
                    else:
                        self.player2_score += 1
                    self.main_window.show_results_screen(self.current_player)
                elif "" not in self.board:
                    self.main_window.show_results_screen(None)
                else:
                    self.current_player = "O" if self.current_player == "X" else "X"
                    self.update_score_label()
                    if self.is_one_player_mode and self.current_player == "O":
                        self.lock_buttons()
                        QTimer.singleShot(500, self.bot_move)  # Delay bot move by 500ms
        return callback

    def bot_move(self):
        # Try to win
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                if self.check_winner():
                    self.buttons[i].setText("O")
                    self.buttons[i].setEnabled(False)
                    self.buttons[i].setStyleSheet("font-size: 24px; background-color: blue; color: black; border-radius: 5px;")
                    self.player2_score += 1
                    self.main_window.show_results_screen("O")
                    self.unlock_buttons()
                    return
                self.board[i] = ""

        # Try to block the opponent
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "X"
                if self.check_winner():
                    self.board[i] = "O"
                    self.buttons[i].setText("O")
                    self.buttons[i].setEnabled(False)
                    self.buttons[i].setStyleSheet("font-size: 24px; background-color: blue; color: black; border-radius: 5px;")
                    self.current_player = "X"
                    self.update_score_label()
                    self.unlock_buttons()
                    return
                self.board[i] = ""

        # Make a random move
        available_moves = [i for i, spot in enumerate(self.board) if spot == ""]
        if available_moves:
            move = random.choice(available_moves)
            self.board[move] = "O"
            self.buttons[move].setText("O")
            self.buttons[move].setEnabled(False)
            self.buttons[move].setStyleSheet("font-size: 24px; background-color: blue; color: black; border-radius: 5px;")
            if self.check_winner():
                self.player2_score += 1
                self.main_window.show_results_screen("O")
            elif "" not in self.board:
                self.main_window.show_results_screen(None)
            else:
                self.current_player = "X"
                self.update_score_label()
        self.unlock_buttons()

    def lock_buttons(self):
        for button in self.buttons:
            button.setEnabled(False)

    def unlock_buttons(self):
        for i, button in enumerate(self.buttons):
            if self.board[i] == "":
                button.setEnabled(True)

    def check_winner(self):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
            [0, 4, 8], [2, 4, 6]             # Diagonal
        ]
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != "":
                return True
        return False

    def reset_board(self):
        self.current_player = "X"
        self.board = [""] * 9
        for button in self.buttons:
            button.setText("")
            button.setEnabled(True)
            button.setStyleSheet("font-size: 24px; background-color: black; color: black; border-radius: 5px;")
        self.update_score_label()