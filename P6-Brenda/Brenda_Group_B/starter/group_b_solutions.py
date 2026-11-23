"""Group B algorithms. ChatGPT assistance declared in README."""


def solve_merge(inst, stats=None):
    a = list(zip(inst['ids'], inst['delay']))
    n = len(a)
    temp = [None] * n
    if stats is not None:
        stats.update(comparisons=0, record_writes=2*n, counter_writes=0)

    def sort_range(lo, hi):
        if hi-lo <= 1:
            return
        # Sort both halves.
        mid = (lo+hi)//2
        sort_range(lo, mid)
        sort_range(mid, hi)
        i, j, k = lo, mid, lo
        while i < mid and j < hi:
            if stats is not None:
                stats['comparisons'] += 1
            # Left wins ties.
            if a[i][1] >= a[j][1]:
                temp[k] = a[i]
                i += 1
            else:
                temp[k] = a[j]
                j += 1
            k += 1
        while i < mid:
            temp[k] = a[i]
            i += 1
            k += 1
        while j < hi:
            temp[k] = a[j]
            j += 1
            k += 1
        for k in range(lo, hi):
            a[k] = temp[k]
        if stats is not None:
            stats['record_writes'] += 2*(hi-lo)

    sort_range(0, n)
    result = [fid for fid, _ in a]
    if stats is not None:
        stats['record_writes'] += n
    return result


def solve_counting(inst, stats=None, min_delay=-60, max_delay=900):
    ids, delays = inst['ids'], inst['delay']
    width = max_delay-min_delay+1
    count = [0]*width
    next_pos = [0]*width
    output = [None]*len(ids)
    if stats is not None:
        stats.update(comparisons=0, record_writes=len(ids), counter_writes=2*width)
    # Shift delays to valid indices.
    for delay in delays:
        index = delay-min_delay
        count[index] += 1
        if stats is not None:
            stats['counter_writes'] += 1
    # Start larger delays first.
    position = 0
    for index in range(width-1, -1, -1):
        next_pos[index] = position
        position += count[index]
        if stats is not None:
            stats['counter_writes'] += 1
    # Forward placement keeps ties stable.
    for i in range(len(ids)):
        index = delays[i]-min_delay
        output[next_pos[index]] = ids[i]
        next_pos[index] += 1
        if stats is not None:
            stats['record_writes'] += 1
            stats['counter_writes'] += 1
    return output


TECHNIQUES = {'merge': solve_merge, 'counting': solve_counting}
