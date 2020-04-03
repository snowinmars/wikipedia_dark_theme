import tabulate  # from local for now
import pprint

required_properties = [
    'date',
    'removed',
    'infected',
    'total',
    '4th_class',
    '5th_class',
    'first_value',
    'first_diff',
    'second_value',
    'second_diff'
]

optional_properties = []


def val_or_none(val):
    return val if bool(val) else None


def parse_row_object(cells):
    row_object = {}

    is_optional_cell = lambda x: "{{=}}" not in x \
                                 and "=" in x

    required_cells = [cell.strip() for cell in cells if not is_optional_cell(cell) and 'Medical cases chart/Row' not in cell]
    optional_cells = [cell.strip() for cell in cells if is_optional_cell(cell)]

    # we shound be sure that we sill not miss any property
    for property in required_properties:
        if property not in row_object:
            row_object[property] = None

    for i, cell in enumerate(required_cells):
        # if optional parameters was misused
        if i == len(required_cells) - 1:
            break

        row_object[required_properties[i]] = val_or_none(cell)

    for i, cell in enumerate(optional_cells):
        # if optional parameters was misused
        if i == len(optional_cells) - 1:
            break

        # optional cell has =
        variable, value = cell.split('=')
        row_object[variable] = value

        if variable not in optional_properties:
            if variable in ['divisor', 'numwidth', 'factor']:
                continue

            optional_properties.append(variable)

            print(f'set {variable} to {value}')

    # ensure that all optional properties exists in all rows
    for property in optional_properties:
        if property not in row_object:
            row_object[property] = None

    return row_object


def parse_rows(rows_data):
    rows = filter(None, rows_data.split('\n'))

    rows_object = []
    for i, row in enumerate(rows):
        # print(f'row {i} starts')

        cells = row.split('|')
        cells[0] = cells[0][2:] # First 2 symbols are {{
        cells[-1] = cells[-1][:-2] # Last 2 symbols are {{

        row_object = parse_row_object(cells)
        # pprint.pprint(row_object)

        rows_object.append(row_object)

        # print(f'row {i} ends')

    return rows_object


rows = '''
{{Medical cases chart/Row| 2020-02-28 |       |         | 1     |    |    | 1        |          |          |          | firstright1=y | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row|            |       |         | 1     |    |    | 1        |          |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-03 |       |         | 4     |    |    | 4        | +300%    |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-04 |       |         | 10    |    |    | 10       | +150%    |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-06 |       |         | 10    |    |    | 10       | +0%      |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-07 |       | 1       | 10    |    |    | 10       | +0%      |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-08 |       | 1       | 10    |    |    | 10       | +0%      |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-09 |       | 1       | 10    |    |    | 10       | +0%      |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-10 |       | 3       | 10    |    |    | 10       | +0%      |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-11 |       | 3       | 10    |    |    | 10       | +0%      |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-12 |       | 3       | 21    |    |    | 21       | +110%    |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-13 |       | 3       | 27    |    |    | 27       | +29%     |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-14 |       | 3       | 27    |    |    | 27       | +0%      |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-15 |       | 3       | 27    |    |    | 27       | +0%      |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-16 |       | 3       | 36    |    |    | 36       | +33%     |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-17 |       | 3       | 36    |    |    | 36       | +0%      |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-18 |       | 5       | 51    |    |    | 51       | +41%     |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-19 |       | 5       | 51    |    |    | 51       | +0%      |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-20 |       | 15      | 69    |    |    | 69       | +35%     |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-21 |       | 15      | 76    |    |    | 76       | +10%     |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-22 |       | 15      | 76    |    |    | 76       | +0%      |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-23 |       | 22      | 81    |    |    | 81       | +6.5%    |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-24 |       | 22      | 81    |    |    | 81       | +0%      |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-25 |       | 29      | 86    |    |    | 86       | +6.2%    |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-26 |       | 29      | 86    |    |    | 86       | +0%      |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-27 |       | 32      | 94    |    |    | 94       | +9.3%    |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-28 |       | 32      | 94    |    |    | 94       | +9.3%    |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-29 |       | 32      | 94    |    |    | 94       | +9.3%    |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-30 |       | 47      | 152   |    |    | 152      | +61%     |          |          |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-03-31 | 1     | 47      | 152   |    |    | 152      | +0%      | 1        |          | firstright2=y | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-04-01 | 2     | 42      | 163   |    |    | 163      | +7.2%    | 1        | {{=}}    |               | divisor=3 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-04-02 | 4     | 42      | 300   |    |    | 300      | +84%     | 1        | {{=}}    |               | divisor=3 | numwidth=mtmw }}
'''

new_data = parse_rows(rows)

set_value_or_space = lambda x: x if x else ' '
set_equals_or_space = lambda x, y: f'{x}={y}' if y else ' '

table = []
for row in parse_rows(rows):
    row_data = []

    for property in required_properties:
        row_data.append(set_value_or_space(row[property]))

    for property in optional_properties:
        row_data.append(set_equals_or_space(property, row[property]))

    table.append(row_data)

print(tabulate.tabulate(table,
                        headers=[*required_properties, *optional_properties],
                        datarow=tabulate.DataRow("", " ; ", ""),
                        linebelowheader=tabulate.Line("", "-", " ; ", ""),
                        headerrow=tabulate.DataRow("", " ; ", "")))
