from os import listdir, path
from json import load
from utils import colors
colors = colors.Colors()


def make_sumbit_unclickable(sumbit_button):
    sumbit_button.setStyleSheet("QPushButton { color: " + colors.white +
                                "; background-color: " + colors.lighter_gray +
                                "; border: 1px solid " + colors.lighter_gray +
                                "; border-radius: 15px; padding: 5px 10px; }")

    sumbit_button.setEnabled(False)
    return sumbit_button


def make_sumbit_clickable(sumbit_button):
    sumbit_button.setStyleSheet("QPushButton { color: " + colors.white +
                                "; background-color: " + colors.darker_gray +
                                "; border-radius: 15px; padding: 5px 10px; }" +
                                "QPushButton:pressed { background-color: " + colors.dark_gray +
                                "; border: 2px solid " + colors.black + "; padding: 0px;}")

    sumbit_button.setEnabled(True)
    return sumbit_button


def services_dict_to_list(ticket_dict, empoyee_name, ticket_time_string):
    lines = []
    for _, service in ticket_dict.items():
        lines.append(f'{empoyee_name},{ticket_time_string},{service[0]},{round(float(service[1]), 2):.2f}')
    return lines


def format_output_string(output_string):
    return output_string + '\n'


def create_daily_output_file(file_path):
    parent_dir = path.dirname(path.abspath(file_path))
    file_name = path.basename(file_path)
    files = listdir(parent_dir)
    if file_name not in files:
        header_row = 'Employee,TicketTime,ServiceName,ServicePrice'
        with open(file_path, 'w') as f:
            f.write(format_output_string(header_row))


def write_lines_to_output_file(file_path, lines):
    # create the output file if it doesn't exist
    create_daily_output_file(file_path)
    # format line strings
    lines = [format_output_string(line) for line in lines]
    # write lines to the file
    with open(file_path, 'a') as f:
        f.writelines(lines)


def get_list_from_json(config_path, config_type):
    assert config_type == 'employees' or config_type == 'services', f'Invalid config type: {config_type}'
    with open(config_path, 'r') as f:
        data = load(f)
    output_list = []
    for item in data:
        if config_type == 'employees':
            output_list.append(item['name'])
        elif config_type == 'services':
            output_list.append((item['name'], item['price']))
        else:
            raise Exception(f'Invalid config type: {config_type}')
    return output_list


def set_error_mode(parent):
    parent.services_total_widget.total_label.setStyleSheet(f'border: None; color: {colors.red};')
    parent.services_total_widget.total_label.setText('ERROR!')
    # make the submit button unclickable
    parent.submit_button_widget.button = make_sumbit_unclickable(parent.submit_button_widget.button)
    return parent
