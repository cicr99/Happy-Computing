from typing import List


def lower_bound(list, item):
    base = -1
    top = len(list)
    while base + 1 < top:
        mid = (base + top) // 2
        if list[mid] < item:
            base = mid
        else:
            top = mid
    return top
