def xnor(*bools):
    """Takes first 2 elements and calc xnor, then use result to calc xnor with 3rd element etc"""
    result = bools[0] == bools[1]
    for b in bools[2:]:
        result = result == b
    return result
