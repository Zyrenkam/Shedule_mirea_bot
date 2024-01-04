import os
# all information sent in this form
# full_info = {'institute': '-', 'kurs': '-', 'group': '-'}


def parse_shedules(info):
    # info = {'institute': 'IPTIP', 'kurs': '2', 'group': 'ЭСБО-01-22'}
    shed_files = os.listdir('shedules')
    cleared_files = []
    print('ALL FILES')
    print(shed_files)

    for file in shed_files:
        if info['institute'] in file:
            cleared_files.append(file)

    shed_files = cleared_files
    cleared_files = []
    for file in shed_files:
        if info['kurs'] in file:
            cleared_files.append(file)

    print('-------------')
    print('POSIBLE FILES')
    print(cleared_files)

    return cleared_files
