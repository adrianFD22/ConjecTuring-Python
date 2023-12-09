
import time
import conjecturing as ct


# Generator 
def sequence_generator(n):
    for i in range(n):
        yield i

# Condition
def sleep_condition(x):
    time.sleep(0.0001)
    return True


# ConjeTuring: testing the package
n = 100001
ct.find_counterexample(n, sleep_condition, sequence_generator(n), True)
