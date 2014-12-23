#!/usr/bin/env python
# usage: ./ukulele.py | sort | more
Maxfret = 4
Ukulele = ['G', 'C', 'E', 'A']
Guitar = ['E', 'A', 'D', 'G', 'B', 'E']
Tuning = Ukulele
Pitches = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
from itertools import *

def rotate(list, n=1):
    if len(list) == 0:
        return list
    n = n % len(list)
    return list[n:] + list[:n]

class Chord:
    
    def __init__(self, fing):
        self.fing = fing
        ##fing2notes
        self.allnotes=[None]*len(fing)
        for i in range(len(fing)):
            self.allnotes[i] = Pitches[ (Pitches.index(Tuning[i]) + fing[i]) % 12 ]
        ##normalize
        self.normnotes=list(set(self.allnotes))
        self.normnotes.sort()
        ##intervals
        self.N = len(self.normnotes)
        self.ps = Pitches
        self.ps.sort()
        self.pitchlist = [None]*self.N
        self.interval_list = [None]*self.N
        for i in range(self.N):
            self.pitchlist[i] = self.ps.index(self.normnotes[i])
        for i in range(self.N):
            self.interval_list[i] = self.pitchlist[(i+1) % self.N] - self.pitchlist[i]
            if self.interval_list[i] < 0:
                self.interval_list[i] += 12
        #decode
        self.chordtype = None
        self.root = None
        for i in range(len(self.interval_list)):
            if self.interval_list == [3,4,5]: self.chordtype = "m"
            elif self.interval_list == [4,3,5]: self.chordtype = ""
            elif self.interval_list == [4,3,3,2]: self.chordtype = "7"
            elif self.interval_list == [4,3,4,1]: self.chordtype = "maj7"
            elif self.interval_list == [3,4,3,2]: self.chordtype = "m7"
            elif self.interval_list == [3,3,6]: self.chordtype = "dim"
            elif self.interval_list == [4,4,4]: self.chordtype = "aug"
            elif self.interval_list == [2,2,3,5]: self.chordtype = "9"
            elif self.interval_list == [5,2,5]: self.chordtype = "sus"
            elif self.interval_list == [7,5]: self.chordtype = "5"
            elif self.interval_list == [3,3,3,3]: self.chordtype = "dim7"
            elif self.interval_list == [3,3,4,2]: self.chordtype = "m7b5"
            elif self.interval_list == [5,2,3,2]: self.chordtype = "7sus"
            # C6 = Am7, etc., so we never mention 6th chords.
            if self.chordtype != None:
                self.root = self.normnotes[0]
                break
            self.interval_list = rotate(self.interval_list)
            self.normnotes = rotate(self.normnotes)

    def print_table_row(self):
        print self.fing, "\t", self.allnotes, "\t", self.interval_list, "\t",
        print self.root, self.chordtype

    def print_short(self):
        if self.chordtype == None:
            pass # unknown chord; do not print
        else:
            self.fingstr = ""
            for i in range(len(self.fing)):
                if i == 0:
                    self.fingstr += str(self.fing[i])
                else:
                    self.fingstr += ","
                    self.fingstr += str(self.fing[i])
            print ' '.join([self.root, self.chordtype]), "\t", self.fingstr

#### main loop

find_these = None
#find_these = ['A#maj7', 'A#7', 'D#', 'D', 'Gm7', 'C7', 'F7sus', 'D#maj7', 'Daug'] # comment out if no search

for f in product(range(0,Maxfret+1), repeat=len(Tuning)):
    c = Chord(f)
    if find_these == None:
        c.print_short() # print all
    else:
        if c.root != None:
            for findme in find_these:
                if ''.join([c.root, c.chordtype]) == findme:
                    c.print_short()

#### tests

fchord=Chord([2,0,1,0])
dmchord=Chord([2,2,1,0])
gmchord=Chord([0,2,3,1])

c7=Chord([0,0,0,1])
cdim7=Chord([2,3,2,3])
caug=Chord([1,0,0,3])
c9=Chord([0,0,0,5])
c9alt=Chord([0,2,0,3])

assert fchord.allnotes == ['A', 'C', 'F', 'A']
assert dmchord.allnotes == ['A', 'D', 'F', 'A']
assert gmchord.allnotes == ['G', 'D', 'G', 'A#']
assert fchord.chordtype == ""
assert dmchord.chordtype == "m"
assert gmchord.chordtype == "m"

assert c7.chordtype == "7"
assert cdim7.chordtype == "dim7"
assert caug.chordtype == "aug"
assert c9.chordtype == "9"
assert c9alt.chordtype == "9"

assert fchord.root == "F"
assert dmchord.root == "D"
assert gmchord.root == "G"
assert c7.root == "C"

# Do not assert root tone of a dim7 because there are four equally
# valid roots. (Or aug: 3 equally valid)

assert c9.root == "C"
assert c9alt.root == "C"
