#!/usr/bin/env python
# usage: ./ukulele.py | sort | more
Maxfret = 4
Ukulele = ['G', 'C', 'E', 'A']
Guitar = ['E', 'A', 'D', 'G', 'B', 'E']
Tuning = Guitar
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

#### main

# for f in product(range(0,Maxfret+1), repeat=len(Tuning)):
#     c = Chord(f)
#     c.print_short()

Tuning = Guitar
f7sus = Chord((1,3,1,3,1,1))
f7sus.print_table_row()

Tuning = Ukulele
f7 = Chord((2,3,1,3))
f7.print_table_row()

f7sus = Chord((3,3,1,3))
f7sus.print_table_row()
