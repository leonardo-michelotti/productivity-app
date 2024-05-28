import sqlite3

from qtpy.QtCore import Qt  # Adicionando a importação do Qt
from qtpy.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class TodoTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadTodos()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.todoInput = QLineEdit()
        self.todoInput.setPlaceholderText("Nova Tarefa To-Do")
        layout.addWidget(self.todoInput)

        addTodoButton = QPushButton("Adicionar To-Do")
        addTodoButton.clicked.connect(self.addTodo)
        layout.addWidget(addTodoButton)

        self.todoList = QListWidget()
        layout.addWidget(self.todoList)

    def addTodo(self):
        todo = self.todoInput.text()
        if todo:
            conn = sqlite3.connect('productivity_app.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO todos (description) VALUES (?)', (todo,))
            conn.commit()
            conn.close()
            self.todoInput.clear()
            self.loadTodos()

    def loadTodos(self):
        self.todoList.clear()
        conn = sqlite3.connect('productivity_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, description FROM todos')
        for todo_id, description in cursor.fetchall():
            listItem = QListWidgetItem(description)
            listItem.setData(Qt.UserRole, todo_id)

            deleteButton = QPushButton('x')
            deleteButton.setFixedSize(20, 20)
            deleteButton.clicked.connect(lambda _, lid=listItem: self.removeTodoItem(lid))

            itemWidget = QWidget()
            itemLayout = QHBoxLayout()
            itemLayout.addWidget(QLabel(description))
            itemLayout.addWidget(deleteButton)
            itemLayout.setContentsMargins(0, 0, 0, 0)
            itemWidget.setLayout(itemLayout)

            listItem.setSizeHint(itemWidget.sizeHint())
            self.todoList.addItem(listItem)
            self.todoList.setItemWidget(listItem, itemWidget)
        conn.close()

    def removeTodoItem(self, listItem):
        todo_id = listItem.data(Qt.UserRole)
        conn = sqlite3.connect('productivity_app.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
        conn.commit()
        conn.close()
        self.todoList.takeItem(self.todoList.row(listItem))
