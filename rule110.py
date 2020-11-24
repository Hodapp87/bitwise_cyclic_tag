#!/usr/bin/env python3

import numpy as np
import PIL.Image

class RepeatCA(object):
    def __init__(self, state, rule):
        self.state = state
        self.state_len = len(state)
        if self.state_len <= 0:
            raise Exception("State must have at least one element")
        self.rule = rule
        self.cases = (
            (self.rule &   1) > 0,
            (self.rule &   2) > 0,
            (self.rule &   4) > 0,
            (self.rule &   8) > 0,
            (self.rule &  16) > 0,
            (self.rule &  32) > 0,
            (self.rule &  64) > 0,
            (self.rule & 128) > 0,
        )
    def get_trajectory(self):
        history = []
        s = self.state
        i = 0
        def idx_or_none(state):
            try:
                return history.index(state)
            except ValueError:
                return None
        while True:
            if i > 0:
                idx = idx_or_none(s)
                if idx is not None:
                    break
            history.append(s)
            s2 = [0] * self.state_len
            for j in range(self.state_len):
                n0 = s[(j - 1) % self.state_len]
                n1 = s[j]
                n2 = s[(j + 1) % self.state_len]
                if self.cases[(n0 << 2) + (n1 << 1) + n2]:
                    s2[j] = 1
            s = s2
            i += 1
        return i - idx, history

class CA(object):
    def __init__(self, rule, state=[], bg=[0]):
        self.rule = rule
        self.state = state
        self.cases = (
            (self.rule &   1) > 0,
            (self.rule &   2) > 0,
            (self.rule &   4) > 0,
            (self.rule &   8) > 0,
            (self.rule &  16) > 0,
            (self.rule &  32) > 0,
            (self.rule &  64) > 0,
            (self.rule & 128) > 0,
        )
        # Determine the trajectory of the background (a background
        # input that is periodic in space with period N is guaranteed
        # to both: iterate to produce only more states periodic in N
        # in space, and be periodic in time with period of <= 2^N):
        rca = RepeatCA(bg, rule=rule)
        period, traj = rca.get_trajectory()
        print("Background input: periodic in space with {} and in time with {}".format(
            rca.state_len, period))
        self.bg_traj = traj
        self.bg_len = rca.state_len
        self.bg_period = period
    def _cell(self, idx):
        l = len(self.state)
        # 0 is the middle of self.state
        idx2 = (l // 2) - idx
        if idx2 < 0 or idx2 >= l:
            return self.bg[idx % self.bg_len]
        else:
            return self.state[idx2]
    def get_initial(self):
        return CAState(self.state, self.bg_traj[0], self.bg_len), 0
    def iterate(self, state, bg_idx):
        l2 = state.horizon + 2
        s2 = [0] * l2
        for i in range(l2):
            i0 = (l2 // 2) - i
            n0 = state.cell(i0 - 1)
            n1 = state.cell(i0 + 0)
            n2 = state.cell(i0 + 1)
            if self.cases[(n0 << 2) + (n1 << 1) + n2]:
                s2[i] = 1
        bg_idx2 = (bg_idx + 1) % self.bg_period
        return CAState(s2, self.bg_traj[bg_idx2], self.bg_len), bg_idx2

class CAState(object):
    def __init__(self, state, bg, bg_len):
        self.state = state
        self.bg = bg
        self.bg_len = bg_len
        self.horizon = len(state)
    def cell(self, idx):
        l = len(self.state)
        # 0 is the middle of self.state
        idx2 = (l // 2) - idx
        if idx2 < 0 or idx2 >= l:
            return self.bg_cell(idx)
        else:
            return self.state[idx2]
    def bg_cell(self, idx):
        return self.bg[idx % self.bg_len]
    def equals_bg(self):
        for i,_ in enumerate(self.state):
            if self.cell(i) != self.bg_cell(i):
                return False
        return True
    def short_str(self, disp_size, shift=0):
        return "".join([
            "*" if self.cell(i) else " "
            for i in range(-disp_size//2 + shift, disp_size//2 + shift)
        ])
    def to_arr(self, width):
        return np.array([
            self.cell(i) for i in range(-width//2, width//2)
        ])
    
def test_run(rule=110, iters=25, state=[1], disp_size=60, shift=0, bg=[0]):
    c = CA(rule=rule, state=state, bg=bg)
    s,b = c.get_initial()
    for i in range(iters):
        print(s.short_str(disp_size, shift=shift))
        s,b = c.iterate(s,b)

def test_run_arr(rule=110, iters=500, state=[1], disp_size=500, bg=[0]):
    arr = np.zeros((iters, disp_size), dtype=np.uint8)
    c = CA(rule=rule, state=state, bg=bg)
    s,b = c.get_initial()
    for i in range(iters):
        arr[i, :] = s.to_arr(disp_size)
        s,b = c.iterate(s,b)
    if s.equals_bg():
        print("State equals background")
    #import pdb; pdb.set_trace()
    return arr

def arr2img(arr, fname):
    img = PIL.Image.fromarray(arr * 255)
    img.save(fname)

# Ether:
ether_bg = [0,0,0,1,0,0,1,1,0,1,1,1,1,1]
