from qtpy.QtCore import Qt, QTime, QTimer  # Importar QTimer de qtpy.QtCore
from qtpy.QtWidgets import QLabel, QLCDNumber, QPushButton, QVBoxLayout, QWidget


class PomodoroTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.timerDisplay = QLCDNumber()
        self.timerDisplay.setDigitCount(8)
        layout.addWidget(self.timerDisplay)

        self.startButton = QPushButton("Iniciar")
        self.startButton.clicked.connect(self.startTimer)
        layout.addWidget(self.startButton)

        self.resetButton = QPushButton("Resetar")
        self.resetButton.clicked.connect(self.resetTimer)
        layout.addWidget(self.resetButton)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTimer)
        self.time = QTime(0, 25, 0)  # Pomodoro padrão: 25 minutos

        self.updateTimer()

    def startTimer(self):
        self.timer.start(1000)  # Atualiza a cada segundo

    def resetTimer(self):
        self.timer.stop()
        self.time = QTime(0, 25, 0)  # Reiniciar para 25 minutos
        self.updateTimer()

    def updateTimer(self):
        self.timerDisplay.display(self.time.toString("hh:mm:ss"))
        if self.time == QTime(0, 0, 0):
            self.timer.stop()
        else:
            self.time = self.time.addSecs(-1)
