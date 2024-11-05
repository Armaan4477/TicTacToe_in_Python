from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QRadioButton, QButtonGroup, QHBoxLayout, QLineEdit, QPushButton
from PyQt6.QtCore import Qt

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