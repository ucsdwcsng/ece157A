# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Wes Packet Rx
# GNU Radio version: 3.8.1.0

from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal




class wes_packet_rx(gr.hier_block2):
    def __init__(self, corr_tag_delay=131, header_len=32, num_skip=8, samp_rate=1e6):
        gr.hier_block2.__init__(
            self, "Wes Packet Rx",
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
                gr.io_signaturev(3, 3, [gr.sizeof_char*1, gr.sizeof_char*1, gr.sizeof_char*1]),
        )

        ##################################################
        # Parameters
        ##################################################
        self.corr_tag_delay = corr_tag_delay
        self.header_len = header_len
        self.num_skip = num_skip
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.samp_symb = samp_symb = 4
        self.rolloff = rolloff = 0.5
        self.const = const = digital.constellation_calcdist(digital.psk_4()[0], digital.psk_4()[1],
        2, 1).base()
        self.preamble_modulator = preamble_modulator = digital.generic_mod(const, False, samp_symb, False, rolloff, False, False)
        self.preamble_hex = preamble_hex = [0xEB, 0x11, 0x9C, 0x33, 0x6C, 0x6A, 0x29, 0x3F, 0x98, 0x34, 0x8E, 0x13, 0x3B, 0xF7, 0x0D, 0x11]
        self.preamble_bit = preamble_bit = [1,1,1,0,1,0,1,1,0,0,0,1,0,0,0,1,1,0,0,1,1,1,0,0,0,0,1,1,0,0,1,1,0,1,1,0,1,1,0,0,0,1,1,0,1,0,1,0,0,0,1,0,1,0,0,1,0,0,1,1,1,1,1,1,1,0,0,1,1,0,0,0,0,0,1,1,0,1,0,0,1,0,0,0,1,1,1,0,0,0,0,1,0,0,1,1,0,0,1,1,1,0,1,1,1,1,1,1,0,1,1,1,0,0,0,0,1,1,0,1,0,0,0,1,0,0,0,1]
        self.num_tag_key = num_tag_key = "bits_per_byte"
        self.nfilts_pfb = nfilts_pfb = 32
        self.modulated_preamble = modulated_preamble = digital.modulate_vector_bc(preamble_modulator .to_basic_block(), preamble_hex, [1])
        self.len_tag_key = len_tag_key = "packet_length"
        self.sliced_modulated_preamble = sliced_modulated_preamble = modulated_preamble[100:]
        self.preamble = preamble = preamble_bit[0:64]
        self.pi = pi = 3.141592654
        self.pfb_filter = pfb_filter = firdes.root_raised_cosine(nfilts_pfb, nfilts_pfb*samp_symb, 1, rolloff, nfilts_pfb*11*samp_symb+1)
        self.header_formatter = header_formatter = digital.packet_header_default(header_len, len_tag_key,num_tag_key,2)

        ##################################################
        # Blocks
        ##################################################
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(samp_symb, 2*pi/200, pfb_filter, nfilts_pfb, int(nfilts_pfb/2), 0.5, 1)
        self.digital_packet_headerparser_b_0_0 = digital.packet_headerparser_b(header_formatter.base())
        self.digital_header_payload_demux_0_0 = digital.header_payload_demux(
            header_len,
            1,
            0,
            "packet_length",
            "corr_est",
            True,
            gr.sizeof_gr_complex,
            "rx_time",
            int(samp_rate),
            (),
            0)
        self.digital_diff_decoder_bb_0_0 = digital.diff_decoder_bb(4)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(4)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(2*pi/200, 4, False)
        self.digital_constellation_decoder_cb_0_0_0_0_0 = digital.constellation_decoder_cb(const)
        self.digital_constellation_decoder_cb_0_0_0_0 = digital.constellation_decoder_cb(const)
        self.blocks_repack_bits_bb_1_0 = blocks.repack_bits_bb(1, 2, "", False, gr.GR_LSB_FIRST)
        self.blocks_repack_bits_bb_1 = blocks.repack_bits_bb(1, 2, "", False, gr.GR_LSB_FIRST)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(2, 8, "packet_length", False, gr.GR_MSB_FIRST)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_message_debug_0 = blocks.message_debug()



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.digital_packet_headerparser_b_0_0, 'header_data'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.digital_packet_headerparser_b_0_0, 'header_data'), (self.digital_header_payload_demux_0_0, 'header_data'))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self, 0))
        self.connect((self.blocks_repack_bits_bb_1, 0), (self.digital_diff_decoder_bb_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_1_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0_0_0, 0), (self.blocks_repack_bits_bb_1_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0_0_0_0, 0), (self.blocks_repack_bits_bb_1, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_header_payload_demux_0_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.digital_packet_headerparser_b_0_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self, 2))
        self.connect((self.digital_diff_decoder_bb_0_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.digital_diff_decoder_bb_0_0, 0), (self, 1))
        self.connect((self.digital_header_payload_demux_0_0, 0), (self.digital_constellation_decoder_cb_0_0_0_0, 0))
        self.connect((self.digital_header_payload_demux_0_0, 1), (self.digital_constellation_decoder_cb_0_0_0_0_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self, 0), (self.digital_pfb_clock_sync_xxx_0, 0))

    def get_corr_tag_delay(self):
        return self.corr_tag_delay

    def set_corr_tag_delay(self, corr_tag_delay):
        self.corr_tag_delay = corr_tag_delay

    def get_header_len(self):
        return self.header_len

    def set_header_len(self, header_len):
        self.header_len = header_len
        self.set_header_formatter(digital.packet_header_default(self.header_len, self.len_tag_key,self.num_tag_key,2))

    def get_num_skip(self):
        return self.num_skip

    def set_num_skip(self, num_skip):
        self.num_skip = num_skip

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_samp_symb(self):
        return self.samp_symb

    def set_samp_symb(self, samp_symb):
        self.samp_symb = samp_symb
        self.set_pfb_filter(firdes.root_raised_cosine(self.nfilts_pfb, self.nfilts_pfb*self.samp_symb, 1, self.rolloff, self.nfilts_pfb*11*self.samp_symb+1))
        self.set_preamble_modulator(digital.generic_mod(self.const, False, self.samp_symb, False, self.rolloff, False, False))

    def get_rolloff(self):
        return self.rolloff

    def set_rolloff(self, rolloff):
        self.rolloff = rolloff
        self.set_pfb_filter(firdes.root_raised_cosine(self.nfilts_pfb, self.nfilts_pfb*self.samp_symb, 1, self.rolloff, self.nfilts_pfb*11*self.samp_symb+1))
        self.set_preamble_modulator(digital.generic_mod(self.const, False, self.samp_symb, False, self.rolloff, False, False))

    def get_const(self):
        return self.const

    def set_const(self, const):
        self.const = const
        self.set_preamble_modulator(digital.generic_mod(self.const, False, self.samp_symb, False, self.rolloff, False, False))

    def get_preamble_modulator(self):
        return self.preamble_modulator

    def set_preamble_modulator(self, preamble_modulator):
        self.preamble_modulator = preamble_modulator

    def get_preamble_hex(self):
        return self.preamble_hex

    def set_preamble_hex(self, preamble_hex):
        self.preamble_hex = preamble_hex

    def get_preamble_bit(self):
        return self.preamble_bit

    def set_preamble_bit(self, preamble_bit):
        self.preamble_bit = preamble_bit
        self.set_preamble(self.preamble_bit[0:64])

    def get_num_tag_key(self):
        return self.num_tag_key

    def set_num_tag_key(self, num_tag_key):
        self.num_tag_key = num_tag_key
        self.set_header_formatter(digital.packet_header_default(self.header_len, self.len_tag_key,self.num_tag_key,2))

    def get_nfilts_pfb(self):
        return self.nfilts_pfb

    def set_nfilts_pfb(self, nfilts_pfb):
        self.nfilts_pfb = nfilts_pfb
        self.set_pfb_filter(firdes.root_raised_cosine(self.nfilts_pfb, self.nfilts_pfb*self.samp_symb, 1, self.rolloff, self.nfilts_pfb*11*self.samp_symb+1))

    def get_modulated_preamble(self):
        return self.modulated_preamble

    def set_modulated_preamble(self, modulated_preamble):
        self.modulated_preamble = modulated_preamble
        self.set_sliced_modulated_preamble(self.modulated_preamble[100:])

    def get_len_tag_key(self):
        return self.len_tag_key

    def set_len_tag_key(self, len_tag_key):
        self.len_tag_key = len_tag_key
        self.set_header_formatter(digital.packet_header_default(self.header_len, self.len_tag_key,self.num_tag_key,2))

    def get_sliced_modulated_preamble(self):
        return self.sliced_modulated_preamble

    def set_sliced_modulated_preamble(self, sliced_modulated_preamble):
        self.sliced_modulated_preamble = sliced_modulated_preamble

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble

    def get_pi(self):
        return self.pi

    def set_pi(self, pi):
        self.pi = pi
        self.digital_costas_loop_cc_0.set_loop_bandwidth(2*self.pi/200)
        self.digital_pfb_clock_sync_xxx_0.set_loop_bandwidth(2*self.pi/200)

    def get_pfb_filter(self):
        return self.pfb_filter

    def set_pfb_filter(self, pfb_filter):
        self.pfb_filter = pfb_filter
        self.digital_pfb_clock_sync_xxx_0.update_taps(self.pfb_filter)

    def get_header_formatter(self):
        return self.header_formatter

    def set_header_formatter(self, header_formatter):
        self.header_formatter = header_formatter
