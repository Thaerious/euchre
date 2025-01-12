# create a delimited string out of a list

def delString(aList, delimiter = ", "):
    sb = ""

    length = len(aList) - 1
    if length < 0: return ""

    for i in range(length):
        item = aList[i]
        sb = sb + str(item) + delimiter

    item = aList[-1]
    sb = sb + str(item)
        
    return sb