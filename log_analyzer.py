#!/usr/bin/env python

def parse_log(logfile):
    '''Reads the logfile and parse it expecting apache/NCSA common log format.
    Returns a generator of tuples of (code, size)'''
    log = open(logfile)
    for line in log.readlines():
        split = line.split()
        code, size = split[-2], split[-1]
        pair = []
        for value in code, size:
            try:
                iv = int(value)
                pair.append(iv)
            except ValueError:
                break
       
        # Throw away bad lines
        if len(pair) > 1: 
            yield(tuple(pair))

def aggregate_log(sizes):
    codes = {}
    for code, size in sizes:
        if not codes.has_key(code):
            codes[code] = []

        codes[code].append(size)
    return codes

def get_median(values):
    sorted_values = sorted(values)
    index = len(sorted_values)
    if index % 2 == 1:
        return sorted_values[index/2]
    else:
        return (sorted_values[index/2] + sorted_values[(index/2)-1]) / 2

def reduce_sizes(aggregated_log):
    res = {}
    for k in aggregated_log.keys():
        res[k] = get_median(aggregated_log[k])

    return res


if __name__ == '__main__':
    logfile = 'sizes.log'
    print reduce_sizes(aggregate_log(parse_log(logfile)))
