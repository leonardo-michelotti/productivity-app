import sqlite3

from qtpy.QtCore import Qt  # Adicionando a importação do Qt
from qtpy.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ReadingListTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadReadingList()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.bookTitleInput = QLineEdit()
        self.bookTitleInput.setPlaceholderText("Título do Livro")
        layout.addWidget(self.bookTitleInput)

        self.bookAuthorInput = QLineEdit()
        self.bookAuthorInput.setPlaceholderText("Autor")
        layout.addWidget(self.bookAuthorInput)

        self.bookPagesInput = QLineEdit()
        self.bookPagesInput.setPlaceholderText("Total de Páginas")
        layout.addWidget(self.bookPagesInput)

        addBookButton = QPushButton("Adicionar Livro")
        addBookButton.clicked.connect(self.addBook)
        layout.addWidget(addBookButton)

        self.readingList = QListWidget()
        layout.addWidget(self.readingList)

    def addBook(self):
        title = self.bookTitleInput.text()
        author = self.bookAuthorInput.text()
        total_pages = self.bookPagesInput.text()
        if title and author and total_pages:
            conn = sqlite3.connect('productivity_app.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO reading_list (title, author, total_pages, pages_read) VALUES (?, ?, ?, 0)', (title, author, total_pages))
            conn.commit()
            conn.close()
            self.loadReadingList()
            self.bookTitleInput.clear()
            self.bookAuthorInput.clear()
            self.bookPagesInput.clear()

    def loadReadingList(self):
        self.readingList.clear()
        conn = sqlite3.connect('productivity_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, author, total_pages, pages_read FROM reading_list')
        for book_id, title, author, total_pages, pages_read in cursor.fetchall():
            progress = int((pages_read / total_pages) * 100) if total_pages else 0
            listItem = QListWidgetItem(f"{title} por {author} - {progress}% concluído")
            listItem.setData(Qt.UserRole, book_id)

            itemWidget = QWidget()
            itemLayout = QVBoxLayout()

            infoLabel = QLabel(f"{title} por {author} - {pages_read}/{total_pages} páginas lidas")
            itemLayout.addWidget(infoLabel)

            progressBar = QProgressBar()
            progressBar.setValue(progress)
            itemLayout.addWidget(progressBar)

            updatePagesInput = QLineEdit()
            updatePagesInput.setPlaceholderText("Páginas lidas")
            itemLayout.addWidget(updatePagesInput)

            updateButton = QPushButton("Atualizar")
            updateButton.clicked.connect(lambda _, bid=book_id, ui=updatePagesInput: self.updatePagesRead(bid, ui))
            itemLayout.addWidget(updateButton)

            deleteButton = QPushButton('x')
            deleteButton.setFixedSize(20, 20)
            deleteButton.clicked.connect(lambda _, lid=listItem: self.removeBookItem(lid))
            itemLayout.addWidget(deleteButton)

            itemWidget.setLayout(itemLayout)

            listItem.setSizeHint(itemWidget.sizeHint())
            self.readingList.addItem(listItem)
            self.readingList.setItemWidget(listItem, itemWidget)
        conn.close()

    def updatePagesRead(self, book_id, updatePagesInput):
        pages_read = updatePagesInput.text()
        if pages_read.isdigit():
            conn = sqlite3.connect('productivity_app.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE reading_list SET pages_read = pages_read + ? WHERE id = ?', (int(pages_read), book_id))
            conn.commit()
            conn.close()
            self.loadReadingList()

    def removeBookItem(self, listItem):
        book_id = listItem.data(Qt.UserRole)
        conn = sqlite3.connect('productivity_app.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM reading_list WHERE id = ?', (book_id,))
        conn.commit()
        conn.close()
        self.readingList.takeItem(self.readingList.row(listItem))
