import datetime

institutes_letters = {'К': 'III', 'И': 'IIT',
                      'Б': 'IK', 'Э': 'IPTIP', 'Т': 'IPTIP',
                      'Р': 'IRI', 'Х': 'ITKHT',
                      'Щ': 'RASPISANIE', 'У': 'ITU', 'Г': 'ITU'}
year_now = int(str(datetime.datetime.now().year)[2::])
month_now = int(str(datetime.datetime.now().month))


def determinate_group(text):
    # АБВГ-01-02 ------------------ ЭСБО   01   22
    name = text.replace(' ', '')
    name = name.replace('\n', '').split('-')
    name[0] = name[0].upper()

    if (len(name[0]) < 4) or (len(name[0]) > 5):
        return '\nНедостаточное или чрезерное количество символов...'
    if name[0][0] not in institutes_letters.keys():
        return '\nТакой группы нет'
    try:
        if int(name[1]) == 0:
            return '\nНеверный порядковый номер группы (первое число)'
        if int(name[2]) > year_now:
            return '\nНеверный год поступления (второе число)'
    except:
        return '\nПосле аббревиатуры группы должны идти два числа'

    return '-'.join(name)


def data_fill(group, full_info):
    full_info['group'] = group

    gr_dt = int(group.split('-')[2])

    #full_info['kurs'] = str(dt_now - gr_dt + 1)
    kurs = year_now - gr_dt
    if month_now >= 9:
        kurs += 1
    full_info['kurs'] = str(kurs)
    full_info['institute'] = institutes_letters[group[0]]

    return True
