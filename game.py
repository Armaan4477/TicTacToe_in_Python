from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QGridLayout, QLabel, QLineEdit, QHBoxLayout, QRadioButton, QButtonGroup, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt, QTimer
import random

class StartScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        title = QLabel("Tic Tac Toe")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")
        layout.addWidget(title)

        self.mode_group = QButtonGroup(self)
        self.one_player_mode = QRadioButton("1 Player")
        self.two_player_mode = QRadioButton("2 Players")
        self.two_player_mode.setChecked(True)
        self.one_player_mode.setStyleSheet("color: black;")
        self.two_player_mode.setStyleSheet("color: black;")
        self.mode_group.addButton(self.one_player_mode)
        self.mode_group.addButton(self.two_player_mode)

        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.one_player_mode)
        mode_layout.addWidget(self.two_player_mode)
        layout.addLayout(mode_layout)

        self.player1_input = QLineEdit()
        self.player1_input.setPlaceholderText("Enter Player 1 Name")
        self.player1_input.setStyleSheet("color: black; background-color: #e0e0e0; border: 1px solid #a0a0a0; border-radius: 5px;")
        layout.addWidget(self.player1_input)

        self.player2_input = QLineEdit()
        self.player2_input.setPlaceholderText("Enter Player 2 Name")
        self.player2_input.setStyleSheet("color: black; background-color: #e0e0e0; border: 1px solid #a0a0a0; border-radius: 5px;")
        layout.addWidget(self.player2_input)

        start_button = QPushButton("Start Game")
        start_button.setStyleSheet("font-size: 18px; padding: 10px; color: black; background-color: #a0a0a0; border: 1px solid #707070; border-radius: 5px;")
        start_button.clicked.connect(self.start_game)
        layout.addWidget(start_button)

        self.setLayout(layout)
        self.update_inputs()

        self.one_player_mode.toggled.connect(self.update_inputs)
        self.two_player_mode.toggled.connect(self.update_inputs)

    def update_inputs(self):
        if self.one_player_mode.isChecked():
            self.player2_input.hide()
        else:
            self.player2_input.show()

    def start_game(self):
        player1_name = self.player1_input.text()
        player2_name = self.player2_input.text() if self.two_player_mode.isChecked() else "Bot"
        self.main_window.start_game(player1_name, player2_name, self.one_player_mode.isChecked())

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
        self.score_label.setText(f"{self.player1_name} (X): {self.player1_score} - {self.player2_name} (O): {self.player2_score}")

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

class ResultsScreen(QWidget):
    def __init__(self, main_window, winner):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        result_text = f"The winner is {winner}!" if winner else "It's a draw!"
        result_label = QLabel(result_text)
        result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_label.setStyleSheet("font-size: 18px; color: black;")
        layout.addWidget(result_label)

        restart_button = QPushButton("Next Round")
        restart_button.setStyleSheet("font-size: 18px; padding: 10px; color: black; background-color: #a0a0a0; border: 1px solid #707070; border-radius: 5px;")
        restart_button.clicked.connect(self.main_window.show_game_screen)
        layout.addWidget(restart_button)

        end_button = QPushButton("End Game")
        end_button.setStyleSheet("font-size: 18px; padding: 10px; color: black; background-color: #a0a0a0; border: 1px solid #707070; border-radius: 5px;")
        end_button.clicked.connect(self.main_window.show_final_scores_screen)
        layout.addWidget(end_button)

        self.setLayout(layout)

class FinalScoresScreen(QWidget):
    def __init__(self, main_window, player1_name, player2_name, player1_score, player2_score):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        final_scores_text = f"Final Scores:\n{player1_name} (X): {player1_score}\n{player2_name} (O): {player2_score}"
        final_scores_label = QLabel(final_scores_text)
        final_scores_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        final_scores_label.setStyleSheet("font-size: 18px; color: black;")
        layout.addWidget(final_scores_label)

        restart_button = QPushButton("Restart")
        restart_button.setStyleSheet("font-size: 18px; padding: 10px; color: black; background-color: #a0a0a0; border: 1px solid #707070; border-radius: 5px;")
        restart_button.clicked.connect(self.main_window.restart_game)
        layout.addWidget(restart_button)

        close_button = QPushButton("Close")
        close_button.setStyleSheet("font-size: 18px; padding: 10px; color: black; background-color: #a0a0a0; border: 1px solid #707070; border-radius: 5px;")
        close_button.clicked.connect(self.main_window.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe")
        self.setFixedSize(400, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.start_screen = StartScreen(self)
        self.game_screen = GameScreen(self)
        self.results_screen = None  # Initialized dynamically based on game outcome
        self.final_scores_screen = None  # Initialized dynamically for final scores

        self.layout.addWidget(self.start_screen)
        self.layout.addWidget(self.game_screen)

        self.start_screen.show()
        self.game_screen.hide()

        self.setStyleSheet("background-color: #d3d3d3;")  # Set a darker gray background color

    def start_game(self, player1_name, player2_name, is_one_player_mode):
        self.game_screen.player1_name = player1_name
        self.game_screen.player2_name = player2_name
        self.game_screen.is_one_player_mode = is_one_player_mode
        self.show_game_screen()

    def show_game_screen(self):
        self.start_screen.hide()
        if (self.results_screen):
            self.results_screen.hide()
        if (self.final_scores_screen):
            self.final_scores_screen.hide()
        self.game_screen.reset_board()
        self.game_screen.show()

    def show_results_screen(self, winner):
        self.results_screen = ResultsScreen(self, winner)
        self.layout.addWidget(self.results_screen)
        self.game_screen.hide()
        self.results_screen.show()

    def show_final_scores_screen(self):
        self.final_scores_screen = FinalScoresScreen(
            self,
            self.game_screen.player1_name,
            self.game_screen.player2_name,
            self.game_screen.player1_score,
            self.game_screen.player2_score
        )
        self.layout.addWidget(self.final_scores_screen)
        if (self.results_screen):
            self.results_screen.hide()
        self.game_screen.hide()
        self.final_scores_screen.show()

    def restart_game(self):
        self.game_screen.player1_score = 0
        self.game_screen.player2_score = 0
        self.final_scores_screen.hide()
        self.start_screen.show()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()