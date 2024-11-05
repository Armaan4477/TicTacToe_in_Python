from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

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