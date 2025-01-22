# create a delimited string out of a list

def del_string(aList, delimiter = ", ", wrap = ''):
    sb = ""

    length = len(aList) - 1
    if length < 0: return ""

    for i in range(length):
        item = aList[i]
        sb = sb + wrap + str(item) + wrap + delimiter

    item = aList[-1]
    sb = sb + wrap + str(item) + wrap
        
    return sb