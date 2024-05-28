import random
import sys

from database import init_db
from eisenhower import EisenhowerTab
from notes import NotesTab
from pomodoro import PomodoroTab
from qtpy.QtCore import Qt
from qtpy.QtGui import QColor, QPalette
from qtpy.QtWidgets import QApplication, QLabel, QTabWidget, QVBoxLayout, QWidget
from quotes import get_random_quote
from reading import ReadingListTab
from todo import TodoTab


class ProductivityApp(QWidget):
    def __init__(self):
        super().__init__()
        init_db()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('App Produtividade')
        self.setGeometry(100, 100, 1000, 800)

        self.setDarkMode()

        mainLayout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background: #444444;
                color: black;
                padding: 10px;
            }
            QTabBar::tab:selected {
                background: #666666;
                color: black;
            }
        """)
        mainLayout.addWidget(self.tabs)

        self.quoteLabel = QLabel("")
        self.quoteLabel.setStyleSheet("font-size: 16px; color: #FFD700; font-weight: bold; margin: 10px;")
        mainLayout.addWidget(self.quoteLabel)

        self.eisenhowerTab = EisenhowerTab()
        self.todoTab = TodoTab()
        self.pomodoroTab = PomodoroTab()
        self.notesTab = NotesTab()
        self.readingListTab = ReadingListTab()

        self.tabs.addTab(self.eisenhowerTab, "Matriz de Eisenhower")
        self.tabs.addTab(self.todoTab, "To Do")
        self.tabs.addTab(self.pomodoroTab, "Pomodoro")
        self.tabs.addTab(self.notesTab, "Notas")
        self.tabs.addTab(self.readingListTab, "Lista de Leitura")

        self.setLayout(mainLayout)
        self.showMotivationalQuote()

    def setDarkMode(self):
        darkPalette = QPalette()
        darkPalette.setColor(QPalette.Window, QColor(53, 53, 53))
        darkPalette.setColor(QPalette.WindowText, Qt.white)
        darkPalette.setColor(QPalette.Base, QColor(25, 25, 25))
        darkPalette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        darkPalette.setColor(QPalette.ToolTipBase, Qt.white)
        darkPalette.setColor(QPalette.ToolTipText, Qt.white)
        darkPalette.setColor(QPalette.Text, Qt.white)
        darkPalette.setColor(QPalette.Button, QColor(53, 53, 53))
        darkPalette.setColor(QPalette.ButtonText, Qt.white)
        darkPalette.setColor(QPalette.BrightText, Qt.red)
        darkPalette.setColor(QPalette.Link, QColor(42, 130, 218))
        darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        darkPalette.setColor(QPalette.HighlightedText, Qt.black)
        darkPalette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
        darkPalette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
        QApplication.setPalette(darkPalette)

        self.setStyleSheet("""
            QWidget {
                background-color: #353535;
                color: white;
            }
            QLineEdit {
                background-color: #555555;
                color: white;
            }
            QTextEdit {
                background-color: #555555;
                color: white;
            }
            QListWidget {
                background-color: #555555;
                color: white;
            }
            QPushButton {
                background-color: #444444;
                color: white;
            }
        """)

    def showMotivationalQuote(self):
        quote = get_random_quote()
        self.quoteLabel.setText(quote)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ProductivityApp()
    ex.show()
    sys.exit(app.exec_())
