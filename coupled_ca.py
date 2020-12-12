#!/usr/bin/env python3

import numpy as np
import PIL.Image

import random

class CoupledCA(object):
    def __init__(self, rule_cases):
        self.rule_cases = rule_cases
    def iterate(self, states):
        s0 = states[0]
        s1 = states[1]
        s0_max = len(s0)
        s1_max = len(s1)
        new_s0 = []
        new_s1 = []
        # This is the number of consecutive 0s.  If we reach the end,
        # these are just not written; if we reach a 1, they are
        # written to new_s0/s1 and it is reset.
        run_0s = 0
        h = max(s0_max, s1_max)
        for i in range(h + 2):
            if i == 0:
                x0 = 0
                y0 = 0
            else:
                x0 = s0[i - 1] if (i - 1) < s0_max else 0
                y0 = s1[i - 1] if (i - 1) < s1_max else 0
            x1 = s0[i] if i < s0_max else 0
            y1 = s1[i] if i < s1_max else 0
            case = (x0 << 3) + (x1 << 2) + (y0 << 1) + (y1 << 0)
            val = self.rule_cases[case]
            if val == 0:
                run_0s += 1
            else:
                new_s0.extend([0]*run_0s)
                new_s0.append(1)
                run_0s = 0
        run_0s = 0
        new_s0_max = len(new_s0)
        h2 = max(new_s0_max, s1_max)
        for i in range(h2 + 2):
            if i == 0:
                x0 = 0
                y0 = 0
            else:
                x0 = new_s0[i - 1] if (i - 1) < new_s0_max else 0
                y0 = s1[i - 1] if (i - 1) < s1_max else 0
            x1 = new_s0[i] if i < new_s0_max else 0
            y1 = s1[i] if i < s1_max else 0
            case = (x0 << 3) + (x1 << 2) + (y0 << 1) + (y1 << 0)
            val = self.rule_cases[case]
            if val == 0:
                run_0s += 1
            else:
                new_s1.extend([0]*run_0s)
                new_s1.append(1)
                run_0s = 0
        return [new_s0, new_s1]

def int2cases(val, bits):
    return tuple(1*(val & (2**i) > 0) for i in range(2**bits))

def print_cases(cases, bits):
    h = ["{:3d}".format(b) for b in range(bits)]
    hdr = " ".join(h) + " | state"
    print(hdr)
    print("-" * len(hdr))
    for i in range(2**bits):
        l = ["{:3d}".format(1 * ((i & (2**b)) > 0)) for b in range(bits)]
        print(" ".join(l) + " | " + str(cases[i]))

def state_str(state):
    return "<" + "".join(["*" if s else " " for s in state]) + ">"

# Example:
test_cases = (
    #      y1  y0  x1  y1
    #####################
    0, #    0   0   0   0
    0, #    0   0   0   1
    0, #    0   0   1   0
    0, #    0   0   1   1
    0, #    0   1   0   0
    0, #    0   1   0   1
    0, #    0   1   1   0
    0, #    0   1   1   1
    0, #    1   0   0   0
    0, #    1   0   0   1
    0, #    1   0   1   0
    0, #    1   0   1   1
    0, #    1   1   0   0
    0, #    1   1   0   1
    0, #    1   1   1   0
    0, #    1   1   1   1
)

def test(rule=None):
    if rule is None:
        while True:
            rule = random.randint(0, 2**16)
            cases = int2cases(rule, 4)
            if cases[0]:
                print("Ignore {}".format(rule))
            else:
                break
    cases = int2cases(rule, 4)
    print("Rule: {:5d}".format(rule))
    ca = CoupledCA(cases)
    # This is arbitrary:
    s0 = [1, 1]
    s1 = [1, 1]
    hist = [(s0, s1)]
    ok = False
    for i in range(50):
        s0, s1 = ca.iterate([s0, s1])
        if len(s0) > 2 or len(s1) > 2:
            ok = True
        hist.append((s0, s1))
    if ok:
        print("State sequence: ")
        for i, (s0, s1) in enumerate(hist):
            print("{:5d} {}".format(i, state_str(s0)))
            print("{:5d} {}".format(i, state_str(s1)))
        return True
    else:
        return False

#for i in range(100):
#    test()

#test(65534)
