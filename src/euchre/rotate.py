
def rotate(list):
    """ move the last item to the first """
    list.append(list.pop(0))

def rotateTo(list, target):
    """ repeatedly move the last item to the first until target is first"""
    while list[0] != target:
        list.append(list.pop(0))