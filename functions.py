import csv

def csv_to_html_table(file_name, start_row, end_row, start_column, end_column):
    with open(file_name, 'r') as file:
        csv_reader = csv.reader(file)
        html_table = '<table>'
        html_thead = '<thead>'
        html_tbody = '<tbody>'

        # первая строка с названиями столбцов
        html_thead += '<tr>'
        for j, element in enumerate(csv_reader.__next__()):
            if start_column <= j <= end_column:
                html_thead += f'<th>{element}</th>'
        html_thead += '</tr>'
        html_thead += '<tr>'

        counter = [0]*end_column
        csv_reader2 = csv.reader(file)
        for i, row in enumerate(csv_reader2):
            if start_row <= i <= end_row:
                html_tbody += '<tr>'
                for j, element in enumerate(row):
                    if start_column <= j <= end_column:
                        if start_row == i:
                            print(element)
                            html_thead += f'<th>{get_type(element)}</th>'
                        html_tbody += f'<td>{element}</td>'
                        if not element:
                            counter[j] += 1
                html_tbody += '</tr>'
        html_thead += '<tr>'
        for j in range(end_column):
            if start_column <= j <= end_column:
                html_thead += f'<td>{str(counter[j])+"/"+str(end_row-start_row+1)}</td>'
        html_thead += '</tr>'
        html_table += html_thead
        html_table += html_tbody
        html_table += '</table>'
        print(counter)
        return html_table

def sort_array(_array, col):
    sorted_array = _array.copy()

    sorted_array.pop(0)
    sorted_array = sorted(sorted_array, key=lambda x: x[col])
    return [_array[0]]+sorted_array


def group_by_column(file_path, column_index):
    groups = {}
    result = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        s = csv_reader.__next__()
        result.append([s[column_index], 'min', 'max', 'avg', 'count'])
        for row in csv_reader:
            column_value = row[column_index]
            if column_value not in groups:
                groups[column_value] = []
            groups[column_value].append(row)

    for key, value in groups.items():
        group_element = ""
        costs = []
        for row in value:
            group_element = row[column_index]
            costs.append(float(row[7]))

        result.append([group_element, min(costs), max(costs), int(sum(costs) / len(value)),len(value)])

    return result

def get_avg_value(csv, col, param):
    group_data = group_by_column(csv, col)
    sort_group_data_count = sort_array(group_data, param)
    slice_data = sort_group_data_count[len(sort_group_data_count) - 5:len(sort_group_data_count):1]
    return slice_data
def group_by_array_column(array,column_index):
    groups = {}
    result = []

    for row in array:
        column_value = row[column_index]
        if column_value not in groups:
            groups[column_value] = []
        groups[column_value].append(row)

    for key, value in groups.items():
        group_element = ""
        costs = []
        for row in value:
            group_element = row[column_index]
            costs.append(float(row[6]))

        result.append([group_element, min(costs), max(costs), int(sum(costs) / len(value)), len(value)])

    return result


def array_to_html(arr):
    html = '<table>'
    for row in arr:
        html += '<tr>'
        for item in row:
            html += '<td>{}</td>'.format(item)
        html += '</tr>'
    html += '</table>'
    return html


def csv_to_array(file_path):
    array = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            array.append(row)
    return array


def get_type(string):
    try:
        number = int(string)
        return "int"
    except ValueError:
        pass
    try:
        number = float(string)
        return "float"
    except ValueError:
        pass
    return "string"