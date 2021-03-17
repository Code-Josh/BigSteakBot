time_str = {'s': 1,
            'm': 60,
            'h': 3600,
            'd': 86400}

def time_to_str(sek):
    d = sek // 86400
    h = (sek % 86400) // 3600
    m = ((sek % 86400) % 3600) // 60
    s = (((sek % 86400) % 3600) % 60)
    str_a = ''
    if d != 0:
        str_a += str(d) + 'd'
    if h != 0:
        str_a += str(h) + 'h'
    if m != 0:
        str_a += str(m) + 'm'
    if s != 0:
        str_a += str(s) + 's'
    return str_a


def str_to_time(str):
    try:
        pos = []
        pos.append(['s', str.find('s')])
        pos.append(['m', str.find('m')])
        pos.append(['h', str.find('h')])
        pos.append(['d', str.find('d')])

        pos_sort = sorted(pos, key=lambda position: position[1])
        timestr = str.replace('s', '#')
        timestr = timestr.replace('m', '#')
        timestr = timestr.replace('h', '#')
        timestr = timestr.replace('d', '#')
        timestr = timestr.split('#')[:-1]
        sek = 0
        a = 0
        for i in range(4 - len(timestr), 4):
            sek += int(timestr[a]) * time_str[pos_sort[i][0]]

        return sek
    except:
        return 0