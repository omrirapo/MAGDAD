
def restrict_to_target(target, obj_arr):
    """
    rstrict search for specific target rect. recieves a rectangle and a list of rectangles and returnes
    a new list of all the rects that intersect it.
    sorted by the size of the intesection
    :param target: (x,y,w,h)
    :param obj_arr: array of rects
    :return: list of rects in obj arr that intersect with target
    """
    if target is None:
        return [(x,0) for x in obj_arr]
    recs = []
    for rec in obj_arr:
        if rec[2] + target[2] < max(rec[0]+rec[2], target[0]+target[2]) - min(rec[0],target[0]) or rec[3] + target[3] < max(rec[1]+rec[3], target[1]+target[3]) - min(rec[1],target[1]):
            recs.append((rec,0))
        else:
            recs.append((rec,1))


    return recs


