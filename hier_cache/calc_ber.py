# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: BER Computation
# Author: wes
# GNU Radio version: 3.8.1.0

from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal




class calc_ber(gr.hier_block2):
    def __init__(self):
        gr.hier_block2.__init__(
            self, "BER Computation",
                gr.io_signaturev(2, 2, [gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1]),
                gr.io_signaturev(2, 2, [gr.sizeof_float*1, gr.sizeof_float*1]),
        )

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.iir_filter_xxx_0_0 = filter.iir_filter_ffd([1], [1, 1], True)
        self.iir_filter_xxx_0 = filter.iir_filter_ffd([1], [1, 1], True)
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_sub_xx_0 = blocks.sub_cc(1)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_cc(0)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.5)
        self.blocks_max_xx_0_0 = blocks.max_ff(1, 1)
        self.blocks_max_xx_0 = blocks.max_ff(1, 1)
        self.blocks_divide_xx_0 = blocks.divide_ff(1)
        self.blocks_complex_to_mag_0_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_cc(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_complex_to_mag_0_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.iir_filter_xxx_0, 0))
        self.connect((self.blocks_complex_to_mag_0_0, 0), (self.iir_filter_xxx_0_0, 0))
        self.connect((self.blocks_divide_xx_0, 0), (self, 0))
        self.connect((self.blocks_max_xx_0, 0), (self.blocks_divide_xx_0, 1))
        self.connect((self.blocks_max_xx_0_0, 0), (self.blocks_divide_xx_0, 0))
        self.connect((self.blocks_max_xx_0_0, 0), (self, 1))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.iir_filter_xxx_0, 0), (self.blocks_max_xx_0_0, 0))
        self.connect((self.iir_filter_xxx_0_0, 0), (self.blocks_max_xx_0, 0))
        self.connect((self, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self, 1), (self.blocks_sub_xx_0, 1))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
