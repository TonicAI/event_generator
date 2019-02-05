# Copyright (c) 2019, Tonic AI Inc.

import bisect, random, math, datetime as dt

MIN_BUCKET_CONTAINMENT = 10
MIN_DEPTH = 3
LAMBDA_DIFF = 0.025

def analyze(events, min_time=None, max_time=None):

    events = sorted(events)
    lambdas = []
    time_bounds = []
    start_idx = 0
    end_idx = len(events)

    if not min_time:
        min_time = events[0]
    if not max_time:
        max_time = events[end_idx-1]

    __compute_subdivision(events, start_idx, end_idx, 0, min_time, max_time, lambdas, time_bounds)

    boundaries = [(tb[1] - tb[0]).total_seconds() for tb in time_bounds]
    return lambdas, boundaries

def __compute_subdivision(events, start_idx, end_idx, depth, min_time, max_time, lambdas, time_bounds):
    boundary_time = min_time + (max_time - min_time) / 2

    event_bisect = bisect.bisect(events, boundary_time, start_idx, end_idx)

    if event_bisect - start_idx > MIN_BUCKET_CONTAINMENT and end_idx - event_bisect > MIN_BUCKET_CONTAINMENT:
        lambda_l = __compute_lambda(events[start_idx : event_bisect])
        lambda_r = __compute_lambda(events[event_bisect : end_idx])

        if depth < MIN_DEPTH or abs((lambda_l - lambda_r) / lambda_r) > LAMBDA_DIFF:
            __compute_subdivision(events, start_idx, event_bisect, depth + 1, min_time, boundary_time, lambdas, time_bounds)
            __compute_subdivision(events, event_bisect, end_idx, depth + 1, boundary_time, max_time, lambdas, time_bounds)
            return


    lambdo = __compute_lambda(events[start_idx : end_idx])
    lambdas.append(lambdo)
    time_bounds.append((min_time, max_time))

def __compute_lambda(events):
    sum_of_differences = 0
    for i in range(1, len(events)):
        sum_of_differences += (events[i] - events[i - 1]).total_seconds()
    return (len(events) - 1) / sum_of_differences


def generate(lambdas, boundaries, start_time, end_time):
    """Generates events according to rate parameters lambdas, between start_time and end_time. time_bounds
       provideds offsets from start_time to switch lambda regimes."""

    regime = 0
    t = start_time
    boundary_start = dt.timedelta(seconds=0)
    while True:
        next_event = dt.timedelta(seconds = -math.log (random.random()) / lambdas[regime])
        if (t + next_event) - start_time > boundaries[regime] + boundary_start:
            boundary_start += boundaries[regime]
            t = start_time + boundary_start
            regime = (regime + 1) % len(lambdas)
        else:
            if t < end_time:
                t += next_event
                yield t
            else:
                break

def read_datetime(datetime_str):
    try:
        format = '%Y-%m-%dT%H:%M:%S.%f'
        return dt.datetime.strptime(datetime_str, format)
    except:
        try:
            format = '%Y-%m-%dT%H:%M:%S'
            return dt.datetime.strptime(datetime_str, format)
        except:
            format = '%Y-%m-%d'
            return dt.datetime.strptime(datetime_str, format)

def parse_args(args):
    args = list(args)
    start_arg_idx = args.index('--start')
    start_arg = args[start_arg_idx + 1]
    start = read_datetime(start_arg)
    end_arg_idx = args.index('--end')
    end_arg = args[end_arg_idx + 1]
    end = read_datetime(end_arg)
    args.remove('--start')
    args.remove(start_arg)
    args.remove('--end')
    args.remove(end_arg)
    return start, end, args
