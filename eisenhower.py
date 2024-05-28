import sqlite3

from qtpy.QtCore import Qt
from qtpy.QtGui import QColor, QPalette
from qtpy.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class EisenhowerTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadTasks()

    def initUI(self):
        layout = QGridLayout()
        self.setLayout(layout)
        self.createQuadrant(layout, '1º Quadrante', 'Faça agora', QColor(230, 230, 250), QColor(220, 20, 60), 0, 0)
        self.createQuadrant(layout, '2º Quadrante', 'Agende', QColor(255, 165, 0), QColor(220, 20, 60), 0, 1)
        self.createQuadrant(layout, '3º Quadrante', 'Delegue', QColor(230, 230, 250), QColor(25, 25, 112), 1, 0)
        self.createQuadrant(layout, '4º Quadrante', 'Elimine', QColor(255, 165, 0), QColor(25, 25, 112), 1, 1)

    def createQuadrant(self, layout, title, action, col_color, row_color, row, col):
        quadrantLayout = QVBoxLayout()

        titleLabel = QLabel(title)
        titleLabel.setStyleSheet(f"background-color: {col_color.name()}; color: black; font-weight: bold; padding: 5px;")
        quadrantLayout.addWidget(titleLabel)

        actionLabel = QLabel(action)
        actionLabel.setStyleSheet("font-weight: bold; font-size: 16px; padding: 10px;")
        quadrantLayout.addWidget(actionLabel)

        taskInput = QLineEdit()
        taskInput.setPlaceholderText('Nova Tarefa')
        quadrantLayout.addWidget(taskInput)

        addButton = QPushButton('Adicionar Tarefa')
        addButton.clicked.connect(lambda: self.addTask(taskInput, title))
        quadrantLayout.addWidget(addButton)

        taskList = QListWidget()
        quadrantLayout.addWidget(taskList)

        quadrantWidget = QWidget()
        quadrantWidget.setAutoFillBackground(True)
        p = quadrantWidget.palette()
        p.setColor(QPalette.Window, row_color)
        quadrantWidget.setPalette(p)
        quadrantWidget.setLayout(quadrantLayout)

        layout.addWidget(quadrantWidget, row, col)

        if not hasattr(self, 'taskLists'):
            self.taskLists = {}
        self.taskLists[title] = taskList

    def addTask(self, taskInput, quadrant):
        task = taskInput.text()
        if task:
            conn = sqlite3.connect('productivity_app.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tasks (description, quadrant) VALUES (?, ?)', (task, quadrant))
            task_id = cursor.lastrowid
            conn.commit()
            conn.close()
            self.addTaskToList(task_id, task, quadrant)
            taskInput.clear()

    def addTaskToList(self, task_id, task, quadrant):
        taskList = self.taskLists[quadrant]
        listItem = QListWidgetItem(task)
        listItem.setData(Qt.UserRole, task_id)

        deleteButton = QPushButton('x')
        deleteButton.setFixedSize(20, 20)
        deleteButton.clicked.connect(lambda: self.removeTask(taskList, listItem))

        itemWidget = QWidget()
        itemLayout = QHBoxLayout()
        itemLayout.addWidget(QLabel(task))
        itemLayout.addWidget(deleteButton)
        itemLayout.setContentsMargins(0, 0, 0, 0)
        itemWidget.setLayout(itemLayout)

        listItem.setSizeHint(itemWidget.sizeHint())
        taskList.addItem(listItem)
        taskList.setItemWidget(listItem, itemWidget)

    def removeTask(self, taskList, listItem):
        task_id = listItem.data(Qt.UserRole)
        conn = sqlite3.connect('productivity_app.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
        taskList.takeItem(taskList.row(listItem))

    def loadTasks(self):
        conn = sqlite3.connect('productivity_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, description, quadrant FROM tasks')
        for task_id, description, quadrant in cursor.fetchall():
            self.addTaskToList(task_id, description, quadrant)
        conn.close()
