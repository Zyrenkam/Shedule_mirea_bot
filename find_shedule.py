import openpyxl


def decoration_shed(shedule):
    temp_odd = []
    temp_even = []

    for i in range(0, len(shedule)):
        for j in range(0, len(shedule[i])):
            if (shedule[i][j] == '') or (shedule[i][j] == 'None'):
                shedule[i][j] = '-'

    for i in range(0, len(shedule)-1, 2):
        temp_even.append(shedule[i])
        temp_odd.append(shedule[i+1])

    # odd / even shedule
    odd_week = {'mon': temp_odd[0:7], 'tue': temp_odd[7:14], 'wed': temp_odd[14:21],
                'thu': temp_odd[21:28], 'fri': temp_odd[28:35], 'sat': temp_odd[35:42]}
    even_week = {'mon': temp_even[0:7], 'tue': temp_even[7:14], 'wed': temp_even[14:21],
                 'thu': temp_even[21:28], 'fri': temp_even[28:35], 'sat': temp_even[35:42]}

    print('odd/even')
    print(odd_week)
    print(even_week)

    return [odd_week, even_week]


def shedule(posible_files, full_info):
    for file in posible_files:
        path = 'shedules/' + file
        wb = openpyxl.load_workbook(path)
        sheet = wb.get_sheet_by_name(wb.sheetnames[0])
        check_presence = False
        for cell in sheet[2]:
            try:
                #проверка, является ли ячейка не None
                current_cell = cell.value.split('(')[0]
                current_cell = current_cell.replace(' ', '')
            except:
                continue

            if full_info['group'] == current_cell:
                check_presence = True
                break
        if not check_presence:
            continue

        # loading all text
        whole_shedule = []
        rows = []
        for i in range(1, 88):
            for row in sheet[i]:
                text = str(row.value)
                if '\n' in text:
                    text = text.replace('\n', ' ')

                if i == 2:
                    if '(' in text:
                        text = text.split('(')[0]
                        text = text.replace(' ', '')
                rows.append(text)
            whole_shedule.append(rows)
            rows = []

        col_number = whole_shedule[1].index(full_info['group'])

        # choosing shedule
        res = []
        for i in range(3, 87):
            res.append([whole_shedule[i][col_number], whole_shedule[i][col_number+1], whole_shedule[i][col_number+2], whole_shedule[i][col_number+3]])
        print('*')
        print(res)
        print('*')
        return decoration_shed(res)
