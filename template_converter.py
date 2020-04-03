import tabulate  # from local for now
import pprint

required_properties = [
    'date',
    'removed',
    'infected',
    'total',
    '4th',
    '5th',
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

    # print(f"cells: {cells}")

    required_cells = [cell.strip() for cell in cells if not is_optional_cell(cell) and 'Medical cases chart/Row' not in cell]
    optional_cells = [cell.strip() for cell in cells if is_optional_cell(cell)]

    # print(f'required_cells: {required_cells}')
    # print(f'optional_cells: {optional_cells}')

    # we shound be sure that we sill not miss any property
    for property in required_properties:
        if property not in row_object:
            row_object[property] = None

    for i, cell in enumerate(required_cells):
        # if optional parameters was misused
        if i == len(required_cells):
            break

        try:
            row_object[required_properties[i]] = val_or_none(cell)
        except:
            print('====')
            print('If you see the error, change "len" to "len - 1" in the if above')
            print('I will think later how to fix it properly')
            print('====')
            raise

    for i, cell in enumerate(optional_cells):
        # optional cell has =
        variable, value = cell.split('=')
        row_object[variable] = value

        if variable not in optional_properties:
            if variable in ['divisor', 'numwidth', 'factor']:
                continue

            optional_properties.append(variable)

            # print(f'set {variable} to {value}')

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

    print(f'len: {len(rows_object)}')

    # ensure that all optional properties exists in all rows
    for row_object in rows_object:
        for property in optional_properties:
            if property not in row_object:
                row_object[property] = None
                # print(f'upset {property}')

    return rows_object


def parse_data(data_data):
    data = filter(None, data_data.split('\n'))

    data_object = []
    for i, dat in enumerate(data):
        # print(f'row {i} starts')

        cells = dat.split(';')

        row_object = parse_row_object(cells)
        # pprint.pprint(row_object)

        data_object.append(row_object)

        # print(f'row {i} ends')

    # ensure that all optional properties exists in all rows
    for row_object in data_object:
        for property in optional_properties:
            if property not in row_object:
                row_object[property] = None

    return data_object


def form(data, parser, printer):
    set_value_or_space = lambda x: x if x else ' '
    set_equals_or_space = lambda x, y: f'{x}={y}' if y else ' '

    table = []
    for row in parser(data):
        row_data = []

        for property in required_properties:
            row_data.append(set_value_or_space(row[property]))

        for property in optional_properties:
            row_data.append(set_equals_or_space(property, row[property]))

        table.append(row_data)

    printer(table)





rows = '''
{{Medical cases chart/Row|2020-03-08|||4|||4|n.a|divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|          |||4|||4|=|divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|2020-03-10|||6|||6|+50%|divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|2020-03-11|1||7|||7|+17%|1||divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|2020-03-12|1||23|||23|+229%|1|+0%|divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|2020-03-13|1||31|||31|+35%|1|+0%|divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|2020-03-14|2||41|||41|+32%|2|+100%|divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|2020-03-15|2||51|||51|+24%|2|+0%|divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|2020-03-16|2||62|||62|+22%|2|+0%|divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|2020-03-17|2||81|||81|+31%|2|+0%|divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|2020-03-18|2||94|||94|+16%|2|+0%|divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|2020-03-19|3||112|||112|+19%|3|+50%|divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|2020-03-20|3|1|127|||127|+13%|3|+0%|divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|2020-03-21|3|3|163|||163|+28%|3|+0%|divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|2020-03-22|3|3|187|||187|+15%|3|+0%|divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|2020-03-23|3|3|201|||201|+7%|3|+0%|divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|2020-03-24|3|3|218|||218|+8%|3|+0%|divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|2020-03-25|3|4|242|||242|+11%|3|+0%|divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|2020-03-26|3|8|264|||264|+9%|3|+0%|divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|2020-03-27|3|9|293|||293|+11%|3|+0%|divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|2020-03-28|7|11|331|||331|+13%|7|+133%|divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|2020-03-29|8|14|346|||346|+5%|8|+14%|divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|2020-03-30|8|17|359|||359|+4%|8|+0%|divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|2020-03-31|8|17|399|||399|+11%|8|+0%|divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|2020-04-01|10|20|422|||422|+6%|10|+25%|divisor=2|numwidth=tttm}}
{{Medical cases chart/Row|2020-04-02|10|25|457|||457|+8%|10|+0%|divisor=2|numwidth=tttm}}
'''

data = '''
2020-01-25;;;1;;;1;firstright1=y
2020-01-26;;;1;;;1;{{=}}
2020-01-27;;;2;;;2;+100%
2020-01-28;;;3;;;3;+50%
;;;3;;;3;collapsed=y;id=jan
2020-01-31;;;4;;;4;+33%
;;;4;;;4;collapsed=y;id=feb
2020-02-04;;;5;;;5;+25%
2020-02-05;;;5;;;5;{{=}}
2020-02-06;;;7;;;7;+40%
;;;7;;;7;collapsed=y;id=feb
2020-02-14;;;8;;;8;+14%
;;1;8;;;8;collapsed=y;id=feb
2020-02-20;;1;9;;;9;+13%
;;4;9;;;9;collapsed=y;id=feb
2020-02-23;;4;10;;;10;+11%
2020-02-24;;4;11;;;11;+10%
2020-02-25;;7;11;;;11;{{=}}
2020-02-26;;7;12;;;12;+9%
2020-02-27;;7;14;;;14;+17%
2020-02-28;;7;16;;;16;+14%
2020-02-29;;7;20;;;20;+25%
2020-03-01;;7;24;;;24;+20%
2020-03-02;;7;27;;;27;+13%
2020-03-03;;7;33;;;33;+22%
2020-03-04;;7;34;;;34;+3%
2020-03-05;;8;48;;;48;+41%
2020-03-06;;8;54;;;54;+13%
2020-03-07;;8;60;;;60;+11%
2020-03-08;;8;67;;;67;+12%
2020-03-09;1;8;79;;;79;+18%
2020-03-10;1;8;97;;;97;+23%
2020-03-11;1;9;118;;;118;+22%
2020-03-12;1;11;159;;;159;+35%
2020-03-13;1;11;198;;;198;+25%
2020-03-14;1;11;254;;;254;+28%
2020-03-15;1;11;338;;;338;+33%
2020-03-16;4;11;441;;;441;+30%
2020-03-17;8;11;598;;;598;+36%
2020-03-18;9;11;728;;;728;+22%
2020-03-19;12;11;873;;;873;+20%
2020-03-20;12;15;1088;;;1,088;+25%
2020-03-21;19;16;1331;;;1,331;+22%
2020-03-22;20;18;1472;;;1,472;+11%
2020-03-23;24;112;2091;;;2,091;+42%
2020-03-24;27;185;2819;;;2,819;+35%
2020-03-25;35;197;3409;;;3,409;+21%
2020-03-26;39;228;4043;;;4,043;+19%
2020-03-27;55;353;4757;;;4,757;+18%
2020-03-28;61;500;5655;;;5,655;+19%
2020-03-29;66;508;6320;;;6,320;+12%
2020-03-30;89;1093;7448;;;7,448;+18%
2020-03-31;101;1196;8591;;;8,591;+15%
2020-04-01;111;1540;9731;;;9,731;+13%
2020-04-02;138;1522;11268;;;11,268;+16%
'''

form(data, lambda r: parse_data(r), lambda table: print(tabulate.tabulate(table,
                                                                          headers=[*required_properties, *optional_properties],
                                                                          datarow=tabulate.DataRow("", " ; ", ""),
                                                                          linebelowheader=tabulate.Line("", "-", " ; ", ""),
                                                                          headerrow=tabulate.DataRow("", " ; ", ""))))

exit()

form(rows, lambda r: parse_rows(r), lambda table: print(tabulate.tabulate(table,
                                                                          headers=[*required_properties, *optional_properties],
                                                                          datarow=tabulate.DataRow("", " ; ", ""),
                                                                          linebelowheader=tabulate.Line("", "-", " ; ", ""),
                                                                          headerrow=tabulate.DataRow("", " ; ", ""))))

exit()


