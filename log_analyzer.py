#!/usr/bin/env python

import os

from flask import Flask, jsonify

# Initialize Flask app
app = Flask(__name__)

# Initiallize log stats store
log_data = {'log_hash': '', 'log_stats': {}}

@app.route('/<int:status_code>')
def get_log_stats(status_code):
    logfile = 'sizes.log'
    log_hash = gen_hash(logfile)
    if log_data['log_hash'] == log_hash:
        results = log_data['log_stats']
    else:
        results = reduce_sizes(aggregate_log(parse_log(logfile)))
        log_data['log_hash'] = log_hash
        log_data['log_stats'] = results
 
    if status_code in results.keys():
        res = {'median_size': results[status_code]}
    else:
        res = {'error': 'Status code %s was not found in log %s' % (status_code, logfile)}

    return jsonify(res)

def gen_hash(fn):
    mtime_str = '%.7f' % os.path.getmtime(fn)
    size_str = str(os.path.getsize(fn))
    return mtime_str + '_' + size_str
        

def parse_log(logfile):
    '''Reads the logfile and parse it expecting apache/NCSA common log format.
    Returns a generator of tuples of (code, size)'''
    log = open(logfile)
    for line in log:
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
    #app.debug = True
    app.run(port=8888)
