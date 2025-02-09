
def rotate(list):
    """ move the last item to the first """
    list.append(list.pop(0))
    return list

def rotateTo(list, target):
    """ repeatedly move the last item to the first until target is first"""    
    if not target in list: raise Exception("Can not rotate list, target not present.")
    while list[0] != target:
        list.append(list.pop(0))

    return list

    