
def convert_str_to_number(x):
    key_num = {'K':1000, 'M':1000000, 'B':1000000000}
    if x.isdigit():
        total_stars = int(x)
    else:
        if len(x) > 1:
            total_stars = float(x[:-1]) * key_num.get(x[-1].upper(), 1)
    return int(total_stars)

print(convert_str_to_number('5.5k'))