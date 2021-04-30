def in_bounds(pos, bounds):
    x, y = pos
    if bounds[0][0] <= x <= bounds[1][0] and bounds[0][1] <= y <= bounds[1][1]:
        return True
    return False
