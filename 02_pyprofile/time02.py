import time

class timewith():
    def __init__(self, name=''):
        self.name = name
        self.start = time.time()

    @property
    def elapsed(self):
        return time.time() - self.start

    def checkpoint(self, name=''):
        print '{timer} {checkpoint} took {elapsed} seconds'.format(
            timer=self.name,
            checkpoint=name,
            elapsed=self.elapsed,
        ).strip()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.checkpoint('finished')
        pass

def get_number():
    for x in xrange(5000000):
        yield x

def expensive_function():
    for x in get_number():
        i = x ^ x ^ x
    return 'some result!'

# prints something like:
# fancy thing done with something took 0.582462072372 seconds
# fancy thing done with something else took 1.75355315208 seconds
# fancy thing finished took 1.7535982132 seconds
with timewith('fancy thing') as timer:
    expensive_function()
    timer.checkpoint('done with something')
    expensive_function()
    expensive_function()
    timer.checkpoint('done with something else')

# or directly
timer = timewith('fancy thing')
expensive_function()
timer.checkpoint('done with something')
