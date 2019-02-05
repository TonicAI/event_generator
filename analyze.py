# Copyright (c) 2019, Tonic AI Inc.

import sys, engine, fileinput, datetime as dt

def print_usage():
    print('Usage:')
    print('$ python analyze.py --start <start_date> --end <end_date> [inputfiles]')
    print('\tinputfiles may be omitted, stdin will be used')
    print('\tstart_date and end_date may be either YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS[.ffffff] format')
    print('output written to out_lambdas.dat and out_boundaries.dat')


def read_input(args):
    return [engine.read_datetime(line.strip()) for line in fileinput.input(args)]

if __name__ == '__main__':
    try:
        start, end, args = engine.parse_args(sys.argv)
    except Exception as e:
        print('Invalid argument.', e)
        print_usage()
        sys.exit(1)


    input_events = read_input(args[1:])
    lambdas, boundaries = engine.analyze(input_events, start, end)

    with open('out_lambdas.dat', 'w') as f:
        for item in lambdas:
            f.write("%s\n" % item)

    with open('out_boundaries.dat', 'w') as f:
        for item in boundaries:
            f.write("%s\n" % item)

