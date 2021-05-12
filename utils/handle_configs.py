def get_employee_list(config_file_path):
    employee_list = []
    with open(config_file_path, 'r') as f:
        for line in f.readlines():
            employee_list.append(line.strip())
    return employee_list


def get_services_list(config_file_path):
    services_list = []
    with open(config_file_path, 'r') as f:
        for line in f.readlines():
            line_list = line.strip().split(',')
            service_name, service_price = line_list
            services_list.append((service_name, service_price))
    return services_list
