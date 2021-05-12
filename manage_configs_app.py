from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
import sys
import json
from functools import partial
# import traceback

from utils.components import HeaderLabel
from utils.helpers import get_employees_list_from_json
from utils import colors
colors = colors.Colors()


class EmployeesButtonGroup(QWidget):
    def __init__(self, parent):
        super(EmployeesButtonGroup, self).__init__()
        self.layout = QVBoxLayout()

        self.widget = QWidget()
        # self.layout.resize(300, 150)
        # self.button_group = QButtonGroup(self.widget)

        employees = get_employees_list_from_json('configs/employees.json')
        for i, employee in enumerate(employees):
            print(f'{i} {employee}')
            button = QPushButton(employee)
            self.layout.addWidget(button)
            button.clicked.connect(partial(parent.employee_slot, i))

        # self.layout.addWidget(self.widget)
        self.setLayout(self.layout)


class GuiWindow(QMainWindow):
    def __init__(self):
        # call parent constructor
        super(GuiWindow, self).__init__()
        self.setWindowTitle("Bar Nails & Spa - Config Manager")
        # top left corner xpos and ypos is 0, 0
        xpos, ypos, width, height = 500, 200, 500, 800
        self.setGeometry(xpos, ypos, width, height)

        # widgets
        self.header_widget = HeaderLabel(self)
        self.employee_button_group = EmployeesButtonGroup(self)

        # central widget
        self.central_widget = QWidget()
        self.central_layout = QGridLayout()

        self.central_layout.addWidget(self.header_widget, 0, 0, 1, 2)
        self.central_layout.addWidget(self.employee_button_group, 1, 0)

        self.central_layout.setContentsMargins(5, 0, 5, 50)
        self.central_widget.setStyleSheet(f'background-color: {colors.lighter_pink}')
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

    def employee_slot(self, i):
        # self.employee_button_group.cs_group.id()
        # print(f'Key id: {self.employee_button_group.button_group.id(object)}')
        print(f'Key id: {i}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = GuiWindow()
    win.show()
    sys.exit(app.exec_())  # cleanly close application when the window closes