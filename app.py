from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import traceback
import datetime

from utils import colors
from utils.components import LeftSideButtons, RightSideFrame, HeaderLabel, service_price_line_edit, service_name_button
from utils.helpers import make_sumbit_clickable, make_sumbit_unclickable, services_dict_to_list, write_lines_to_output_file, get_list_from_json, set_error_mode

employees = get_list_from_json('configs/employees.json', 'employees')
services = get_list_from_json('configs/services.json', 'services')
colors = colors.Colors()


class GuiWindow(QMainWindow):
    def __init__(self):
        # call parent constructor
        super(GuiWindow, self).__init__()
        self.setWindowTitle("Your Service Business - Ticket Manager")
        # top left corner xpos and ypos is 0, 0
        xpos, ypos, width, height = 500, 200, 500, 800
        self.setGeometry(xpos, ypos, width, height)

        # widgets
        self.header_widget = HeaderLabel(self)
        self.employee_button_widget = LeftSideButtons(self, employees, 2, 'employee')
        self.service_button_widget = LeftSideButtons(self, [service_tuple[0] for service_tuple in services], 2, 'service')
        self.right_frame_widget = RightSideFrame(self)

        # central widget
        self.central_widget = QWidget()
        self.central_layout = QGridLayout()

        self.central_layout.addWidget(self.header_widget, 0, 0, 1, 2)
        self.central_layout.addWidget(self.employee_button_widget, 1, 0)
        self.central_layout.addWidget(self.service_button_widget, 2, 0)
        self.central_layout.addWidget(self.right_frame_widget, 1, 1, 2, 1)

        self.central_layout.setContentsMargins(5, 0, 5, 50)
        self.central_widget.setStyleSheet(f'background-color: {colors.white}')
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

        # class variables, these get reset on sumbit_pressed
        self.employee = ''
        self.services = {}
        self.service_objects = {}
        self.service_button_index = 0
        self.service_rows_added = 0
        self.services_total = 0
        self.tip = 0.

        date_string = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
        self.output_file_path = f'data/tickets_{date_string}.csv'

    def remove_service_row(self, grid_layout, widgets_to_remove):
        try:
            item_id = None
            for widget in widgets_to_remove:
                # find item_id from button object name
                object_name = widget.objectName()
                object_type = object_name.split('_')[0]
                if object_type == 'button':
                    item_id = int(object_name.split('_')[1])

                # remove widget from grid layout
                grid_layout.removeWidget(widget)
                widget.deleteLater()
                del widget

            # remove service item from self.services
            self.services.pop(item_id)

            # remove service item from self.service_objects
            self.service_objects.pop(item_id)

            # update service total
            self.update_services_total()

        except:
            traceback.print_exc()

    def employee_pressed(self, i):
        self.employee = employees[i]
        self.right_frame_widget.ticket_employee_widget.label.setText(self.employee)
        self.right_frame_widget.ticket_employee_widget.label.setStyleSheet(f'color: {colors.darker_gray}; border: None;')
        font = QFont()
        font.setFamily("Script MT Bold")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.right_frame_widget.ticket_employee_widget.label.setFont(font)

        # add some margin so the Employee: label lines up with the name
        self.right_frame_widget.ticket_employee_widget.title_label.setContentsMargins(0, 15, 0, 0)

        # make the submit button clickable now if there are services and a valid tip
        self.update_services_total()

    def service_price_changed(self, line_edit_widget):
        # use the object_index and replace that tuple(service_name, service_price) with the same service_name and new price
        try:
            object_name = line_edit_widget.objectName()
            object_index = int(object_name.split('_')[1])
            self.services[object_index] = (self.services[object_index][0], line_edit_widget.text())

            # update service total
            self.update_services_total()
        except:
            traceback.print_exc()

    def update_total_label(self):
        self.right_frame_widget.services_total_widget.total_label.setText('${:,.2f}'.format(self.services_total))
        self.right_frame_widget.services_total_widget.total_label.setStyleSheet(f'border: None; color: {colors.darker_gray};')

    def update_services_total(self):
        self.services_total = 0.

        if len(self.services) == 0:
            # this gets triggered by submit_pressed when services get set to zero
            self.update_total_label()
        else:
            try:
                for _id, service_tuple in self.services.items():
                    service_price = float(service_tuple[1])
                    self.services_total += service_price
                    self.services_total = round(self.services_total, 2)

                    self.update_total_label()

                    # update tip because we can use the same ValueError from above
                    self.tip = round(float(self.right_frame_widget.tip_widget.line_edit.text()), 2)

                    # make sure the submit button is clickable if there's a valid employee
                    if self.employee != '':
                        self.right_frame_widget.submit_button_widget.button = make_sumbit_clickable(self.right_frame_widget.submit_button_widget.button)

                    if service_price < 0 or self.tip < 0:
                        self.right_frame_widget = set_error_mode(self.right_frame_widget)

            except ValueError:  # if the typed in price is blank call the price zero, turn the total red, and make submit unclickable to let the user know
                self.right_frame_widget = set_error_mode(self.right_frame_widget)

    def service_pressed(self, i):
        service_name, service_price = services[i]

        font = QFont()
        font.setFamily("verdana")
        font.setPointSize(12)

        # create button and line edit widgets and add them to the ticket_services_widget layout
        line_edit = service_price_line_edit(self, service_price)
        button = service_name_button(self, service_name, line_edit)

        # add button and line_edit to the layout
        self.right_frame_widget.ticket_services_widget.layout.addWidget(button, self.service_rows_added, 0)
        self.right_frame_widget.ticket_services_widget.layout.addWidget(line_edit, self.service_rows_added, 1)
        self.service_rows_added += 1

        # update self.service_objects so I can remove these when submit is pressed
        self.service_objects[self.service_button_index] = (button, line_edit)

        # update self.services
        self.services[self.service_button_index] = (service_name, service_price)
        self.service_button_index += 1

        # update service total
        self.update_services_total()

        # make tip widget visible
        self.right_frame_widget.tip_widget.setVisible(True)

    def tip_changed(self):
        try:
            self.tip = round(float(self.right_frame_widget.tip_widget.line_edit.text()), 2)
            # this will handle any errors
            self.update_services_total()
        except ValueError:
            self.right_frame_widget = set_error_mode(self.right_frame_widget)

    def submit_clicked(self):
        # write self.services to self.output_file_path
        # it's assumed that self.employee is valid because the user can't click submit without first choosing an employee
        ticket_time_string = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S')
        lines = services_dict_to_list(self.services, self.employee, ticket_time_string)
        # add tip line if there is a tip
        if self.tip > 0:
            lines = lines + [f'{self.employee},{ticket_time_string},__TIP__,{self.tip:.2f}']
        write_lines_to_output_file(self.output_file_path, lines)

        # reset employee on ticket
        self.right_frame_widget.ticket_employee_widget.default_employee()

        # remove ticket items from app
        # update_services_total is called inside remove_service_row so two birds
        for i in list(sorted(self.service_objects.keys())):
            object_tuple = self.service_objects[i]
            self.remove_service_row(self.right_frame_widget.ticket_services_widget.layout, object_tuple)

        # hide TipWidget and change visable tip back to zero
        self.right_frame_widget.tip_widget.line_edit.setText('0.00')
        self.right_frame_widget.tip_widget.setVisible(False)

        # make submit unclickable
        self.right_frame_widget.submit_button_widget.button = make_sumbit_unclickable(self.right_frame_widget.submit_button_widget.button)

        # reset class variables
        self.employee = ''
        self.services = {}
        self.service_objects = {}
        self.service_button_index = 0
        self.service_rows_added = 0
        self.services_total = 0
        self.tip = 0.

        date_string = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
        self.output_file_path = f'data/tickets_{date_string}.csv'



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = GuiWindow()
    win.show()
    sys.exit(app.exec_())  # cleanly close application when the window closes
