from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QGridLayout, QLabel
from PyQt6.QtCore import Qt

class StartScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        title = QLabel("Tic Tac Toe")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        start_button = QPushButton("Start Game")
        start_button.clicked.connect(self.main_window.show_game_screen)
        layout.addWidget(start_button)

        self.setLayout(layout)

class GameScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_player = "X"
        self.board = [""] * 9
        self.setup_ui()

    def setup_ui(self):
        layout = QGridLayout()
        self.buttons = []

        for i in range(9):
            button = QPushButton()
            button.setFixedSize(80, 80)
            button.clicked.connect(self.make_move(i))
            self.buttons.append(button)
            layout.addWidget(button, i // 3, i % 3)

        self.setLayout(layout)

    def make_move(self, index):
        def callback():
            if self.board[index] == "" and not self.check_winner():
                self.board[index] = self.current_player
                self.buttons[index].setText(self.current_player)
                if self.check_winner():
                    self.main_window.show_results_screen(self.current_player)
                elif "" not in self.board:
                    self.main_window.show_results_screen(None)
                else:
                    self.current_player = "O" if self.current_player == "X" else "X"
        return callback

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

class ResultsScreen(QWidget):
    def __init__(self, main_window, winner):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        result_text = f"The winner is {winner}!" if winner else "It's a draw!"
        result_label = QLabel(result_text)
        result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(result_label)

        restart_button = QPushButton("Restart")
        restart_button.clicked.connect(self.main_window.show_game_screen)
        layout.addWidget(restart_button)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe")
        self.setFixedSize(300, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.start_screen = StartScreen(self)
        self.game_screen = GameScreen(self)
        self.results_screen = None  # Initialized dynamically based on game outcome

        self.layout.addWidget(self.start_screen)
        self.layout.addWidget(self.game_screen)

        self.start_screen.show()
        self.game_screen.hide()

    def show_game_screen(self):
        self.start_screen.hide()
        if self.results_screen:
            self.results_screen.hide()
        self.game_screen.reset_board()
        self.game_screen.show()

    def show_results_screen(self, winner):
        self.results_screen = ResultsScreen(self, winner)
        self.layout.addWidget(self.results_screen)
        self.game_screen.hide()
        self.results_screen.show()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()