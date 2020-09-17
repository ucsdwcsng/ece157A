# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Pulse Shaping Block (Hier)
# GNU Radio version: 3.8.1.0

from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
import numpy as np




class pulse_shape_hier(gr.hier_block2):
    def __init__(self, bFilter=1, rect_taps=(1,1,1,1,1,1,1,1), roll_off=0.7, sps=4):
        gr.hier_block2.__init__(
            self, "Pulse Shaping Block (Hier)",
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.bFilter = bFilter
        self.rect_taps = rect_taps
        self.roll_off = roll_off
        self.sps = sps

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.rrc_filter = rrc_filter = firdes.root_raised_cosine(4, sps, 1, roll_off, 32*sps+1)

        ##################################################
        # Blocks
        ##################################################
        self.interp_fir_filter_xxx_1_0 = filter.interp_fir_filter_ccc(sps, rect_taps)
        self.interp_fir_filter_xxx_1_0.declare_sample_delay(0)
        self.interp_fir_filter_xxx_1 = filter.interp_fir_filter_ccc(sps, rrc_filter)
        self.interp_fir_filter_xxx_1.declare_sample_delay(0)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccc(1, rrc_filter)
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.blocks_selector_0_0 = blocks.selector(gr.sizeof_gr_complex*1,bFilter,0)
        self.blocks_selector_0_0.set_enabled(True)
        self.blocks_multiply_const_vxx_0_0_0 = blocks.multiply_const_cc(2)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.5)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.blocks_selector_0_0, 0))
        self.connect((self.blocks_selector_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_selector_0_0, 1))
        self.connect((self.interp_fir_filter_xxx_1, 0), (self.blocks_selector_0_0, 2))
        self.connect((self.interp_fir_filter_xxx_1, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.interp_fir_filter_xxx_1_0, 0), (self.blocks_multiply_const_vxx_0_0_0, 0))
        self.connect((self, 0), (self.interp_fir_filter_xxx_1, 0))
        self.connect((self, 0), (self.interp_fir_filter_xxx_1_0, 0))

    def get_bFilter(self):
        return self.bFilter

    def set_bFilter(self, bFilter):
        self.bFilter = bFilter
        self.blocks_selector_0_0.set_input_index(self.bFilter)

    def get_rect_taps(self):
        return self.rect_taps

    def set_rect_taps(self, rect_taps):
        self.rect_taps = rect_taps
        self.interp_fir_filter_xxx_1_0.set_taps(self.rect_taps)

    def get_roll_off(self):
        return self.roll_off

    def set_roll_off(self, roll_off):
        self.roll_off = roll_off
        self.set_rrc_filter(firdes.root_raised_cosine(4, self.sps, 1, self.roll_off, 32*self.sps+1))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rrc_filter(firdes.root_raised_cosine(4, self.sps, 1, self.roll_off, 32*self.sps+1))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_rrc_filter(self):
        return self.rrc_filter

    def set_rrc_filter(self, rrc_filter):
        self.rrc_filter = rrc_filter
        self.interp_fir_filter_xxx_0.set_taps(self.rrc_filter)
        self.interp_fir_filter_xxx_1.set_taps(self.rrc_filter)
