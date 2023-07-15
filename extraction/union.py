def union_list(a, b):
    for value in b:
        if value not in a:
            a.append(value)
    return a

def union_dict(a, b):
    for key in b.keys():
        if key in a:
            union_list(a[key], b[key])
        else:
            a[key] = b[key]
    return a

def union_double_dict(a, b):
    for key in b.keys():
        if key in a:
            union_dict(a[key], b[key])
        else:
            a[key] = b[key]
    return a
