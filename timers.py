import time
import timeit


def clock_timer(func):
    def timer(*args, **kwargs):
        """a decorator which prints execution time of the decorated function"""
        t1 = time.clock()
        result = func(*args, **kwargs)
        t2 = time.clock()
        print("%s executed in %.4f seconds" % (func.__name__, (t2 - t1)))
        log(t2-t1)
        return result
    return timer


def time_timer(func):
    def timer(*args, **kwargs):
        """a decorator which prints execution time of the decorated function"""
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print("%s executed in %.4f seconds" % (func.__name__, (t2 - t1)))
        log(t2-t1)
        return result
    return timer


def timeit_timer(func):
    def timer(*args, **kwargs):
        """a decorator which prints execution time of the decorated function"""
        measured_time = timeit.timeit(lambda: func(*args, **kwargs))
        print("%s executed in %.4f seconds" % (func.__name__, measured_time))
        return measured_time
    return timer


def log(value):
    with open('data.txt', 'a+') as f:
        f.write(str(value) + ",")


def delog():
    data = []
    with open('data.txt', 'r') as f:
        for line in f.readlines():
            data.append([float(number) for number in line.split(",")[:-1]])
    return data