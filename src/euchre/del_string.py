# create a delimited string out of a list

def del_string(a_list, delimiter=", ", wrap=""):
    sb = ""

    length = len(a_list) - 1
    if length < 0:
        return ""

    for i in range(length):
        item = a_list[i]
        sb = sb + wrap + str(item) + wrap + delimiter

    item = a_list[-1]
    sb = sb + wrap + str(item) + wrap

    return sb
