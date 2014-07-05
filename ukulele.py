#!/usr/bin/env python
Maxfret = 2 # 12
Tuning = ['g', 'c', 'e', 'a']
Pitches = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
from itertools import *

def fing2notes(fing):
    notes=[None]*len(fing)
    for i in range(len(fing)):
        notes[i] = Pitches[ (Pitches.index(Tuning[i]) + fing[i]) % 12 ]
    return notes

def normalize(chord):
    chord=list(set(chord))
    chord.sort()
    return chord

def intervals(chord):
    chord = normalize(chord)
    N = len(chord)
    ps = Pitches
    ps.sort()
    pitchlist = [None]*N
    interval_list = [None]*N
    for i in range(N):
        pitchlist[i] = ps.index(chord[i])
    for i in range(N):
        interval_list[i] = pitchlist[(i+1) % N] - pitchlist[i]
        if interval_list[i] < 0:
            interval_list[i] += 12
    return interval_list

def rotate(list, n=1):
    if len(list) == 0:
        return list
    n = n % len(list)
    return list[n:] + list[:n]

def decode_intervals(inter):
    for i in range(len(inter)):
        if inter == [3,4,5]: return "minor"
        elif inter == [4,3,5]: return "major"
        elif inter == [4,3,3,2]: return "seventh"
        inter = rotate(inter)

for f in product(range(0,Maxfret+1), repeat=4):
    print f, "\t", fing2notes(f), "\t", intervals(fing2notes(f)),
    print decode_intervals(intervals(fing2notes(f)))

#### tests

f_fing=[2,0,1,0]
dm_fing=[2,2,1,0]
gm_fing=[0,2,3,1]

assert fing2notes(f_fing) == ['a', 'c', 'f', 'a']
assert fing2notes(dm_fing) == ['a', 'd', 'f', 'a']
assert fing2notes(gm_fing) == ['g', 'd', 'g', 'a#']
