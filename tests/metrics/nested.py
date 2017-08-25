"""
    @author ksdme
    tests the nested type cheked assigment performance
"""

from time import time
from sure.types import string
from sure.builder import TypedModel, prop

CYCLES = 25000

class Sample(TypedModel):
    name = prop({
        "last": string()})

# initial assignment
start, init_accum = 0.0, 0.0
for _ in xrange(CYCLES):
    sample = Sample()

    start = time()
    sample.name.last = "ksdme"
    init_accum += (time() - start)
init_accum /= CYCLES

# reassignment
start, sample = time(), Sample()
for _ in xrange(CYCLES):
    sample.name.last = "ksdme"
accum = (time() - start)/CYCLES

template = "{0}: {1:.8f} Seconds;"
print template.format("Initial Assignment\t", init_accum)
print template.format("Reassignment\t\t", accum)
