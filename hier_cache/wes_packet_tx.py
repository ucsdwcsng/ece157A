# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Wes Packet Tx
# GNU Radio version: 3.8.1.0

from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
import math
import pmt




class wes_packet_tx(gr.hier_block2):
    def __init__(self, cw_len=64, payload_len=255, samp_rate=1e6):
        gr.hier_block2.__init__(
            self, "Wes Packet Tx",
                gr.io_signature(1, 1, gr.sizeof_char*1),
                gr.io_signaturev(6, 6, [gr.sizeof_gr_complex*1, gr.sizeof_char*1, gr.sizeof_char*1, gr.sizeof_char*1, gr.sizeof_char*1, gr.sizeof_char*1]),
        )

        ##################################################
        # Parameters
        ##################################################
        self.cw_len = cw_len
        self.payload_len = payload_len
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.num_tag_key = num_tag_key = "packet_num"
        self.len_tag_key = len_tag_key = "packet_length"
        self.header_len = header_len = 32
        self.throttle_rate = throttle_rate = 100e3
        self.tag_s = tag_s = gr.tag_utils.python_to_tag((0, pmt.intern(len_tag_key), pmt.from_long(payload_len), pmt.intern("vect_test_src")))
        self.tag0 = tag0 = gr.tag_utils.python_to_tag((0, pmt.intern(len_tag_key), pmt.from_long(cw_len), pmt.intern("vect_cw_src")))
        self.sync_seq = sync_seq = [1, 1, -1, 1, -1, 1, 1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1, 1, 1, -1, 1, 1, -1, -1, -1, -1, 1, 1, -1, -1, 1, 1, 1, -1, -1, 1, 1, 1, -1, -1, 1, -1, -1, 1, -1, 1, -1, 1, -1, -1, -1, 1, -1, 1, 1, -1, -1, -1, 1, 1, 1, 1, 1, 1]
        self.sync_len = sync_len = 63
        self.sym_table = sym_table = [-1, 1]
        self.pi = pi = 3.141592654
        self.header_formatter = header_formatter = digital.packet_header_default(header_len, len_tag_key,num_tag_key,1)
        self.diff_mod = diff_mod = 4
        self.cw = cw = int((cw_len/4))*[1,0,1,0]
        self.const = const = digital.constellation_calcdist(digital.psk_4()[0], digital.psk_4()[1],
        2, 1).base()

        ##################################################
        # Blocks
        ##################################################
        self.digital_packet_headergenerator_bb_0_0 = digital.packet_headergenerator_bb(header_formatter.formatter(), len_tag_key)
        self.digital_glfsr_source_x_0 = digital.glfsr_source_b(6, True, 0, 1)
        self.digital_diff_encoder_bb_0_0 = digital.diff_encoder_bb(2)
        self.digital_diff_encoder_bb_0 = digital.diff_encoder_bb(2)
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc((-1,1), 1)
        self.blocks_vector_source_x_0_0 = blocks.vector_source_b(cw, True, 1, [tag0])
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, len_tag_key, 0)
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_char * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_stream_to_tagged_stream_1 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, sync_len, "packet_length")
        self.blocks_stream_to_tagged_stream_0_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, payload_len, len_tag_key)
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, header_len, len_tag_key)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(1, 1, "packet_length", False, gr.GR_LSB_FIRST)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_diff_encoder_bb_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self, 5))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_0_0, 0), (self.digital_diff_encoder_bb_0_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_0_0, 0), (self.digital_packet_headergenerator_bb_0_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_1, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.blocks_stream_to_tagged_stream_1, 0), (self, 2))
        self.connect((self.blocks_tag_gate_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self, 1))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self, 0))
        self.connect((self.digital_diff_encoder_bb_0, 0), (self.blocks_tagged_stream_mux_0, 2))
        self.connect((self.digital_diff_encoder_bb_0, 0), (self, 4))
        self.connect((self.digital_diff_encoder_bb_0_0, 0), (self.blocks_tagged_stream_mux_0, 3))
        self.connect((self.digital_diff_encoder_bb_0_0, 0), (self, 3))
        self.connect((self.digital_glfsr_source_x_0, 0), (self.blocks_stream_to_tagged_stream_1, 0))
        self.connect((self.digital_packet_headergenerator_bb_0_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self, 0), (self.blocks_stream_to_tagged_stream_0_0_0, 0))

    def get_cw_len(self):
        return self.cw_len

    def set_cw_len(self, cw_len):
        self.cw_len = cw_len
        self.set_cw(int((self.cw_len/4))*[1,0,1,0] )
        self.set_tag0(gr.tag_utils.python_to_tag((0, pmt.intern(self.len_tag_key), pmt.from_long(self.cw_len), pmt.intern("vect_cw_src"))))

    def get_payload_len(self):
        return self.payload_len

    def set_payload_len(self, payload_len):
        self.payload_len = payload_len
        self.set_tag_s(gr.tag_utils.python_to_tag((0, pmt.intern(self.len_tag_key), pmt.from_long(self.payload_len), pmt.intern("vect_test_src"))))
        self.blocks_stream_to_tagged_stream_0_0_0.set_packet_len(self.payload_len)
        self.blocks_stream_to_tagged_stream_0_0_0.set_packet_len_pmt(self.payload_len)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_num_tag_key(self):
        return self.num_tag_key

    def set_num_tag_key(self, num_tag_key):
        self.num_tag_key = num_tag_key
        self.set_header_formatter(digital.packet_header_default(self.header_len, self.len_tag_key,self.num_tag_key,1))

    def get_len_tag_key(self):
        return self.len_tag_key

    def set_len_tag_key(self, len_tag_key):
        self.len_tag_key = len_tag_key
        self.set_header_formatter(digital.packet_header_default(self.header_len, self.len_tag_key,self.num_tag_key,1))
        self.set_tag0(gr.tag_utils.python_to_tag((0, pmt.intern(self.len_tag_key), pmt.from_long(self.cw_len), pmt.intern("vect_cw_src"))))
        self.set_tag_s(gr.tag_utils.python_to_tag((0, pmt.intern(self.len_tag_key), pmt.from_long(self.payload_len), pmt.intern("vect_test_src"))))

    def get_header_len(self):
        return self.header_len

    def set_header_len(self, header_len):
        self.header_len = header_len
        self.set_header_formatter(digital.packet_header_default(self.header_len, self.len_tag_key,self.num_tag_key,1))
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.header_len)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.header_len)

    def get_throttle_rate(self):
        return self.throttle_rate

    def set_throttle_rate(self, throttle_rate):
        self.throttle_rate = throttle_rate

    def get_tag_s(self):
        return self.tag_s

    def set_tag_s(self, tag_s):
        self.tag_s = tag_s

    def get_tag0(self):
        return self.tag0

    def set_tag0(self, tag0):
        self.tag0 = tag0
        self.blocks_vector_source_x_0_0.set_data(self.cw, [self.tag0])

    def get_sync_seq(self):
        return self.sync_seq

    def set_sync_seq(self, sync_seq):
        self.sync_seq = sync_seq

    def get_sync_len(self):
        return self.sync_len

    def set_sync_len(self, sync_len):
        self.sync_len = sync_len
        self.blocks_stream_to_tagged_stream_1.set_packet_len(self.sync_len)
        self.blocks_stream_to_tagged_stream_1.set_packet_len_pmt(self.sync_len)

    def get_sym_table(self):
        return self.sym_table

    def set_sym_table(self, sym_table):
        self.sym_table = sym_table

    def get_pi(self):
        return self.pi

    def set_pi(self, pi):
        self.pi = pi

    def get_header_formatter(self):
        return self.header_formatter

    def set_header_formatter(self, header_formatter):
        self.header_formatter = header_formatter

    def get_diff_mod(self):
        return self.diff_mod

    def set_diff_mod(self, diff_mod):
        self.diff_mod = diff_mod

    def get_cw(self):
        return self.cw

    def set_cw(self, cw):
        self.cw = cw
        self.blocks_vector_source_x_0_0.set_data(self.cw, [self.tag0])

    def get_const(self):
        return self.const

    def set_const(self, const):
        self.const = const
