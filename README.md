# Event Timestamp Generator

These programs implement the algorithm presented in our blog post, Synthesizing Realistic Timestamps.
There are two many programs, `analyze.py` and `generate.py`. The only requirement is Python 3.5+.

## analyze.py

`analyze.py` takes a sorted list of timestamps and fits an adaptive, non-homogeneous sequence of
exponential distributions to that data. The output is two files, out_lambdas.dat and out_boundaries.dat
that are meant to be used with `generate.py`. Here's an example of running `analyze.py`.

```
$ python analyze.py --start 2019-02-04 --end 2019-02-05 test_data.dat
```

`--start` and `--end` are the domain of the input data. `test_data.dat` is a sample of
one day of events provided as an example.

# generate.py

`generate.py` takes the output of `analyze.py` and a time range, and synthesizes events with that model.
Here's an example of running `generate.py`

```
$ python generate.py --start 2019-01-01 --end 2019-01-30 out_lambdas.dat out_boundaries.dat
```

Notice that the `--start` and `--end` times don't need to overlap with original data. You can generate as
much data as you want from the model.
