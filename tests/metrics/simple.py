"""
    @author ksdme
    tests the simple type checked assignment
"""
from time import time
from sure.types import string
from sure.builder import prop, TypedModel

CYCLES = 25000

class Sample(TypedModel):
    name = prop(string())

# inital assignment incurs some additional
# steps, thus measure it separately
init_accum = 0.0
for _ in xrange(CYCLES):
    sample = Sample()

    start = time()
    sample.name = "ksdme"
    init_accum += time()-start
init_accum /= CYCLES

# re-assignment test
start, sample = time(), Sample()
for _ in xrange(CYCLES):
    sample.name = "ksdme"
accum = (time() - start)/CYCLES

# general object attr assignment
class Sample2(object):
    pass

start, sample = time(), Sample2()
for _ in xrange(CYCLES):
    sample.name = "ksdme"
general_accum = (time() - start)/CYCLES

# property based assignment
def _internal(self, val):
    self._val = val

class Sample3(object):
    name = property(lambda self: None, _internal)

start, sample = time(), Sample3()
for _ in xrange(CYCLES):
    sample.name = "ksdme"
prop_accum = (time() - start)/CYCLES

# print the results
template = "{0}: {1:.8f} Seconds; (x{2:.2f})"
print template.format("Initial Assignment\t", init_accum, (init_accum/general_accum))
print template.format("Reassignment\t\t", accum, (accum/general_accum))
print template.format("General Assignmnet\t", general_accum, 1)
print template.format("Property Assignmnet\t", prop_accum, prop_accum/general_accum)
