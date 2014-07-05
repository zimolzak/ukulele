#!/usr/bin/env python
Maxfret = 12
Tuning = ['g', 'c', 'e', 'a']
Pitches = ['c', 'c#', 'd', 'eb', 'e', 'f', 'f#', 'g', 'g#', 'a', 'bb', 'b']
from itertools import *

NumChords=0
for p in product(range(0,Maxfret+1), repeat=4):
    NumChords += 1
print NumChords

def fing2notes(fing):
    notes=[None]*len(fing)
    for i in range(len(fing)):
        notes[i]=Pitches[Pitches.index(Tuning[i]) + fing[i]]
    return notes

#### tests

f_fing=[2,0,1,0]
dm_fing=[2,2,1,0]
gm_fing=[0,2,3,1]

assert fing2notes(f_fing) == ['a', 'c', 'f', 'a']
assert fing2notes(dm_fing) == ['a', 'd', 'f', 'a']
assert fing2notes(gm_fing) == ['g', 'd', 'g', 'bb']