def restrict_to_target(target, obj_arr):
    """
    rstrict search for specific target rect. recieves a rectangle and a list of rectangles and returnes
    a new list of all the rects that intersect it.
    sorted by the size of the intesection
    :param target: (x,y,w,h)
    :param obj_arr: array of rects
    :return: list of rects in obj arr that intersect with target
    """
    inside = {}
    top = target[1]
    bot = target[1]+target[3]
    lef = target[0]
    rig = target[0]+target[2]
    for rec in obj_arr:
        rt = rec[1]
        rb = rec[1] + rec[3]
        rl = rec[0]
        rr = rec[0] + rec[2]
        if rt > bot or rb < top or rl > rig or rr < lef:
            pass
        else:
            width = target[2] + rec[2] -(max(rig,rr)-min(lef,rl))
            hight = target[3] + rec[3] -(max(bot,rb)-min(top,rt))
            val = width*hight
            inside[rec] = val
    sorted_recs = sorted(inside.items(), key=lambda x: x[1], reverse=True)
    return sorted_recs


