import tabulate  # from local for now
import pprint
import re

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

    required_cells = [cell.strip() for cell in cells if "=" not in cell and 'Medical cases chart' not in cell]
    optional_cells = [cell.strip() for cell in cells if "=" in cell]

    # we shound be sure that we sill not miss any property
    for property in [*required_properties, *optional_properties]:
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
            optional_properties.append(variable)

        print(f'set {variable} to {value}')

    return row_object


def parse_rows(rows_data):
    rows = filter(None, rows_data.split('\n'))

    rows_object = []
    for i, row in enumerate(rows):
        print(f'row {i} starts')

        cells = row.split('|')
        cells[0] = cells[0][2:] # First 2 symbols are {{
        cells[-1] = cells[-1][:-2] # Last 2 symbols are {{

        row_object = parse_row_object(cells)
        pprint.pprint(row_object)

        rows_object.append(row_object)

        print(f'row {i} ends')
        print()

    return rows_object


rows = '''
{{Medical cases chart/Row| 2020-01-31 |       |         | 2     |    |    | 2        |          |          |               | firstright1=y | factor=13 | numwidth=mtmw }}
{{Medical cases chart/Row|            |       | 2       |       |    |    | 2        |          |          |               |               | factor=13 | numwidth=mtmw }}
{{Medical cases chart/Row| 2020-04-02 | 30    | 235     | 3548  |    |    | 3548     | +28%     | 30       |+6){{nbsp}}(25%|               | factor=13 | numwidth=mtmw }}
'''

data = '''
2020-01-20   ;    ;     ; 1    ; ; ; 1    ; firstright1=y
; 2020-01-31 ;    ;     ; 2    ; ; ; 2    ;      ;    ;                 ; firstright1=y ;
;            ;    ; 2   ;      ; ; ; 2    ;      ;    ;                 ;               ;
; 2020-04-02 ; 30 ; 235 ; 3548 ; ; ; 3548 ; +28% ; 30 ; +6){{nbsp}}(25% ;               ;
'''

new_data = parse_rows(rows)

print()
print(rows)
print()
print(data)
print()

c = lambda x: x if x else ' '
d = lambda x, y: f'{x}={y}' if y else ' '

table = []
for row in parse_rows(rows):
    row_data = []

    for property in required_properties:
        row_data.append(c(row[property]))

    for property in optional_properties:
        row_data.append(d(property, row[property]))

    table.append(row_data)

print(tabulate.tabulate(table, headers=[*required_properties, *optional_properties], datarow=tabulate.DataRow("", " ; ", ""), headerrow=tabulate.DataRow("", " ; ", "")))
