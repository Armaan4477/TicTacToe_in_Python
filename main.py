from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from pregame import StartScreen
from game import GameScreen
from postgame import ResultsScreen, FinalScoresScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe")
        self.setFixedSize(410, 500)

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