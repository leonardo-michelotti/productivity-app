import sqlite3

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class NotesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadNotes()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.noteInput = QTextEdit()
        self.noteInput.setPlaceholderText("Digite sua nota aqui...")
        layout.addWidget(self.noteInput)

        addNoteButton = QPushButton("Adicionar Nota")
        addNoteButton.clicked.connect(self.addNote)
        layout.addWidget(addNoteButton)

        self.notesList = QListWidget()
        layout.addWidget(self.notesList)

    def addNote(self):
        note_content = self.noteInput.toPlainText()
        if note_content:
            conn = sqlite3.connect('productivity_app.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO notes (content) VALUES (?)', (note_content,))
            conn.commit()
            conn.close()
            self.noteInput.clear()
            self.loadNotes()

    def loadNotes(self):
        self.notesList.clear()
        conn = sqlite3.connect('productivity_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, content FROM notes')
        for note_id, content in cursor.fetchall():
            listItem = QListWidgetItem(content)
            listItem.setData(Qt.UserRole, note_id)

            deleteButton = QPushButton('x')
            deleteButton.setFixedSize(20, 20)
            deleteButton.clicked.connect(lambda _, lid=listItem: self.removeNoteItem(lid))

            itemWidget = QWidget()
            itemLayout = QHBoxLayout()
            itemLayout.addWidget(QLabel(content))
            itemLayout.addWidget(deleteButton)
            itemLayout.setContentsMargins(0, 0, 0, 0)
            itemWidget.setLayout(itemLayout)

            listItem.setSizeHint(itemWidget.sizeHint())
            self.notesList.addItem(listItem)
            self.notesList.setItemWidget(listItem, itemWidget)
        conn.close()

    def removeNoteItem(self, listItem):
        note_id = listItem.data(Qt.UserRole)
        conn = sqlite3.connect('productivity_app.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        conn.commit()
        conn.close()
        self.notesList.takeItem(self.notesList.row(listItem))
