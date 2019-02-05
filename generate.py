# Copyright (c) 2019, Tonic AI Inc.

import engine, sys, datetime as dt

def print_usage():
    print('Usage:')
    print("$ python generate.py --start <start_date> --end <end_date> <input_lambdas> <input_boundaries>")
    print('\tstart_date and end_date may be either YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS[.ffffff] format')
    print('\tinput_lambdas and input_boundaries come from analyze.py\'s output')
    print('output printed to stdout')

def read_file(file):
    with open(file, 'r') as f:
        for line in f.readlines():
            yield line


if __name__ == "__main__":

    try:
        start, end, args = engine.parse_args(sys.argv)
    except Exception as e:
        print('Invalid argument.', e)
        print_usage()
        sys.exit(1)

    if (len(args) < 3):
        print_usage()
        sys.exit(1)

    lambdas = [float(lambdo) for lambdo in read_file(args[1])]
    boundaries = [dt.timedelta(seconds = float(s)) for s in read_file(args[2])]

    today = dt.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    events = engine.generate(lambdas, boundaries, start, end)

    for e in events:
        print(e)
