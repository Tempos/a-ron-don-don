import csv
from database import view_data, get_all
from helpers import number_format

# ToDo move to config
report_output_file = "report.csv"
delimiter = ','


headers = view_data + ('2-nd ph', '3-rd ph', '4-th ph', '5-th ph', '6-th ph',
                       '7-th ph',)

with open(report_output_file, 'w', encoding='cp1251') as csv_file:
    writer = csv.DictWriter(
        csv_file, fieldnames=headers, delimiter=delimiter, lineterminator='\n')
    writer.writeheader()

    for __line in get_all():
        _line = list(__line[1:])
        numbers = _line[0].split('\n')
        _line[0] = number_format(numbers[0])
        if len(numbers) != 1:
            [_line.append(number_format(item)) for item in numbers[1:]]

        writer.writerow(dict(zip(headers, _line)))
