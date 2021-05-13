import cairo
import numpy as np
from numpy.core.numeric import zeros_like

class CreateUSAF():
    def __init__(self, bar_width, bar_height, groups=1, scale=1):
        self.bar_w = bar_width
        self.bar_h = bar_height
        self.scale = scale
        self.groups = groups
        self.bar_count = 5
    
    # New version
    def create_group(self, scale=1):
        # rows = self.bar_h
        group_bar_w = np.int(np.ceil(self.bar_w/scale))
        cols = group_bar_w*self.bar_count
        rows = cols

        row = np.zeros(cols, dtype=np.uint8)
        for i in range(5):
            if i%2 == 0:
                continue
            start_ix = i*group_bar_w
            end_ix = start_ix+group_bar_w
            row[start_ix:end_ix] = 255
        group = np.zeros((rows, cols), dtype=np.uint8)
        for i in range(rows):
            group[i] = row
        return group

    def create_raster(self):
        spacer = np.zeros((self.bar_h*2, self.bar_w*2), dtype=np.uint8)
        spacer.fill(255)

        chart_h = spacer.copy()
        chart_v = spacer.copy()

        dummy_h = np.zeros((self.bar_h*2, self.bar_w*(self.bar_count + 1)), dtype=np.uint8)
        dummy_h.fill(255)

        scale = 1
        
        for g in range(self.groups):
            chart_mid = dummy_h.shape[0]//2
            v_bot = chart_mid - self.bar_h//3
            h_top = chart_mid + self.bar_h//3

            group_h = self.create_group(scale=scale)
            group_v = group_h.T
            dummy_h[v_bot-group_h.shape[0]:v_bot, :group_h.shape[1]] = group_h
            dummy_h[h_top:h_top+group_h.shape[0], :group_h.shape[1]] = group_v
            chart_h = np.hstack((chart_h, dummy_h, spacer))
            dummy_h = np.zeros((self.bar_h*2, group_h.shape[1]))
            dummy_h.fill(255)

            scale *= self.scale
        return chart_h

    # Old version
    def create_group_old(self, scale=1):
        rows = self.bar_h
        group_bar_w = np.int(np.ceil(self.bar_w/scale))
        cols = group_bar_w*self.bar_count

        row = np.zeros(cols, dtype=np.uint8)
        for i in range(5):
            if i%2 == 0:
                continue
            start_ix = i*group_bar_w
            end_ix = start_ix+group_bar_w
            row[start_ix:end_ix] = 255
        group = np.zeros((rows, cols), dtype=np.uint8)
        for i in range(rows):
            group[i] = row
        return group

    def create_raster_old(self):
        spacer = np.zeros((self.bar_h, self.bar_w*2), dtype=np.uint8)
        spacer.fill(255)

        usaf = spacer.copy()
        scale = 1
        for g in range(self.groups):
            usaf = np.hstack((usaf, self.create_group_old(scale=scale), spacer.copy()))
            scale *= self.scale
        return usaf