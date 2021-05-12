from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from functools import partial

from utils.helpers import make_sumbit_unclickable
from utils import colors
colors = colors.Colors()


class LeftSideButtons(QFrame):
    def __init__(self, parent, button_list, max_cols, service_or_employee):
        super(LeftSideButtons, self).__init__()
        self.layout = QGridLayout()

        row = 0
        col = 0
        for i, item in enumerate(button_list):
            self.button = QPushButton(item)
            font = QFont()
            font.setFamily("verdana")
            font.setPointSize(14)
            self.button.setFont(font)
            self.button.setStyleSheet("QPushButton { color: " + colors.darker_gray +
                                      "; border: 1px solid " + colors.darker_gray +
                                      "; background-color: " + colors.white +
                                      "; border-radius: 15px; padding: 5px 10px; }QPushButton:pressed { background-color: " + colors.lightest_gray +
                                      "; border: 2px solid " + colors.gray + "; padding: 0px;}")

            if service_or_employee == 'service':
                self.button.clicked.connect(partial(parent.service_pressed, i))  # use partial so that we can include the button id
            elif service_or_employee == 'employee':
                self.button.clicked.connect(partial(parent.employee_pressed, i))
            else:
                print('Buttons need to be service or employee')

            self.layout.addWidget(self.button, row, col)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        self.setStyleSheet(f'border: 1px solid {colors.darker_gray}; border-radius: 10px;')
        self.setLayout(self.layout)


class RightSideFrame(QFrame):
    def __init__(self, parent):
        super(RightSideFrame, self).__init__()
        self.layout = QGridLayout()

        self.ticket_employee_widget = TicketEmployee(self)
        self.layout.addWidget(self.ticket_employee_widget, 0, 0)

        self.ticket_services_widget = TicketServices(self)
        self.layout.addWidget(self.ticket_services_widget, 1, 0)

        self.services_total_widget = ServicesTotal(self)
        self.layout.addWidget(self.services_total_widget, 2, 0)

        self.tip_widget = TipWidget(self)
        # self.tip_widget.line_edit.textChanged.connect(partial(parent.tip_changed, self.tip_widget.line_edit))
        self.tip_widget.line_edit.textChanged.connect(parent.tip_changed)
        self.tip_widget.setVisible(False)
        self.layout.addWidget(self.tip_widget, 3, 0)

        self.submit_button_widget = SubmitTicketButton(self)
        # have to connect the button in this frame because it has access to the parent widget, where self.submit_button_widget does not
        self.submit_button_widget.button.clicked.connect(parent.submit_clicked)
        self.layout.addWidget(self.submit_button_widget, 4, 0)

        self.setStyleSheet(f'border: 1px solid {colors.darker_gray}; border-radius: 10px;')
        self.setLayout(self.layout)


class TicketEmployee(QWidget):
    def __init__(self, parent):
        super(TicketEmployee, self).__init__()
        self.layout = QGridLayout()

        self.font = QFont()
        self.font.setFamily("verdana")
        self.font.setPointSize(14)
        self.font.setBold(True)
        self.font.setWeight(75)

        self.title_label = QLabel()
        self.title_label.setText('Employee:')
        self.title_label.setFont(self.font)
        self.title_label.setStyleSheet(f'color: {colors.darker_gray}; border: None;')
        self.title_label.setAlignment(Qt.AlignRight)
        self.title_label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))

        self.label = QLabel()
        self.default_employee()
        self.label.setAlignment(Qt.AlignHCenter)
        self.label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))

        self.layout.addWidget(self.title_label, 0, 0)
        self.layout.addWidget(self.label, 0, 1)
        self.setLayout(self.layout)

    def default_employee(self):
        self.label.setText('Choose Employee')
        self.label.setStyleSheet(f'color: {colors.red}; border: None;')
        self.label.setFont(self.font)

        self.title_label.setContentsMargins(0, 0, 0, 0)


class ServicesTotal(QWidget):
    def __init__(self, parent):
        super(ServicesTotal, self).__init__()
        self.layout = QGridLayout()

        font = QFont()
        font.setFamily("verdana")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)

        self.static_label = QLabel()
        self.static_label.setText('Total:')
        self.static_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.static_label.setStyleSheet('border: None;')
        self.static_label.setFont(font)

        self.total_label = QLabel()
        self.total_label.setText('${:,.2f}'.format(0.0))
        self.total_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.total_label.setStyleSheet('border: None;')
        self.total_label.setFont(font)

        self.layout.addWidget(self.static_label, 0, 0)
        self.layout.addWidget(self.total_label, 0, 1)
        self.setLayout(self.layout)


class SubmitTicketButton(QWidget):
    def __init__(self, parent):
        super(SubmitTicketButton, self).__init__()
        self.layout = QGridLayout()

        self.button = QPushButton('Submit Ticket')
        font = QFont()
        font.setFamily("verdana")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.button.setFont(font)
        self.button.setMaximumWidth(200)
        self.button = make_sumbit_unclickable(self.button)

        self.layout.addWidget(self.button)
        self.setLayout(self.layout)


class HeaderLabel(QWidget):
    def __init__(self, parent):
        super(HeaderLabel, self).__init__()
        self.layout = QHBoxLayout()

        self.label = QLabel()
        self.label.setText('Your Service Business')
        font = QFont()
        font.setFamily("Script MT Bold")
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet(f'color: {colors.darker_gray};')
        self.label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.label)
        self.setLayout(self.layout)


class TicketServices(QWidget):
    def __init__(self, parent):
        super(TicketServices, self).__init__()
        self.layout = QGridLayout()
        self.setLayout(self.layout)


class TipWidget(QWidget):
    def __init__(self, parent):
        super(TipWidget, self).__init__()
        self.layout = QHBoxLayout()

        self.line_edit = QLineEdit('0.00')
        # self.line_edit.textChanged.connect(partial(parent.tip_changed, self.line_edit))
        self.line_edit = apply_service_line_edit_style(self.line_edit)

        self.tip_label = QLabel('Tip')
        self.tip_label.setAlignment(Qt.AlignCenter)
        self.tip_label = apply_service_button_style(self.tip_label)

        self.layout.addWidget(self.tip_label)
        self.layout.addWidget(self.line_edit)
        self.setLayout(self.layout)


def service_line_font():
    font = QFont()
    font.setFamily("verdana")
    font.setPointSize(12)
    return font


def apply_service_line_edit_style(line_edit):
    line_edit.setAlignment(Qt.AlignCenter)
    line_edit.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred))
    line_edit.setMaximumHeight(50)
    line_edit.setFont(service_line_font())
    line_edit.setStyleSheet(f'background-color: {colors.white};')
    return line_edit


def apply_service_button_style(button):
    button.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
    button.setMaximumHeight(50)
    button.setFont(service_line_font())
    button.setStyleSheet("QPushButton { color: " + colors.darker_gray +
                         "; background-color: " + colors.light_pink +
                         "; border: 1px solid " + colors.light_gray + "; border-radius: 10px; padding: 5px 5px; }")
    return button


def service_price_line_edit(parent, service_price):
    line_edit = QLineEdit(service_price)
    line_edit.setObjectName(f'price_{parent.service_button_index}')
    line_edit.textChanged.connect(partial(parent.service_price_changed, line_edit))
    return apply_service_line_edit_style(line_edit)


def service_name_button(parent, service_name, line_edit_object):
    button = QPushButton(service_name)
    button.setObjectName(f'button_{parent.service_button_index}')
    # attach self.remove_service_row callback to each button so they can be removed with a click
    button.pressed.connect(partial(parent.remove_service_row, parent.right_frame_widget.ticket_services_widget.layout, (button, line_edit_object)))
    return apply_service_button_style(button)
