def delString(aList):
    sb = ""

    for item in aList:
        sb = sb + str(item) + ","

    if sb.endswith(","):
        sb = sb[:-1]
        
    return sb