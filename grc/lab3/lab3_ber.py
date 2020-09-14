#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Lab3 BER
# GNU Radio version: 3.8.1.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt5 import Qt
from gnuradio import qtgui
import sip
from calc_ber import calc_ber  # grc-generated hier_block
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from pulse_shape_hier import pulse_shape_hier  # grc-generated hier_block
from wes_packet_tx import wes_packet_tx  # grc-generated hier_block
import epy_module_0  # embedded python module
import iio
import numpy as np
import pmt
from gnuradio import qtgui

class lab3_ber(gr.top_block, Qt.QWidget):

    def __init__(self, corr_tag_delay=131):
        gr.top_block.__init__(self, "Lab3 BER")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Lab3 BER")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "lab3_ber")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.corr_tag_delay = corr_tag_delay

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 4
        self.snr_default = snr_default = 8.5
        self.rolloff = rolloff = 0.5
        self.payload_len = payload_len = 31
        self.num_tag_key = num_tag_key = "packet_num"
        self.nfilts_pfb = nfilts_pfb = 32
        self.mark_delays = mark_delays = [0, 0, 34, 56, 87, 119]
        self.len_tag_key = len_tag_key = "packet_length"
        self.header_len = header_len = 32
        self.cw_len = cw_len = 32
        self.tag_s = tag_s = gr.tag_utils.python_to_tag((0, pmt.intern(len_tag_key), pmt.from_long(payload_len), pmt.intern("vect_test_src")))
        self.tag0 = tag0 = gr.tag_utils.python_to_tag((0, pmt.intern(len_tag_key), pmt.from_long(cw_len), pmt.intern("vect_cw_src")))
        self.sync_seq = sync_seq = [1, 1, -1, 1, -1, 1, 1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1, 1, 1, -1, 1, 1, -1, -1, -1, -1, 1, 1, -1, -1, 1, 1, 1, -1, -1, 1, 1, 1, -1, -1, 1, -1, -1, 1, -1, 1, -1, 1, -1, -1, -1, 1, -1, 1, 1, -1, -1, -1, 1, 1, 1, 1, 1, 1]
        self.snr_db = snr_db = snr_default
        self.samp_rate = samp_rate = 1e3
        self.rrc_filter = rrc_filter = firdes.root_raised_cosine(4, sps, 1, rolloff, 32*sps+1)
        self.pn_order = pn_order = np.round(np.log2(payload_len+1))
        self.pn6_padded = pn6_padded = [1, 1, 1, 1, 1, 1, -1, 1, -1, 1, -1, 1, 1, -1, -1, 1, 1, -1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, 1, -1, -1, 1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, 1, -1, -1, 1, -1, 1, -1, -1, -1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1 -1 -1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.pn6 = pn6 = [1, 1, 1, 1, 1, 1, -1, 1, -1, 1, -1, 1, 1, -1, -1, 1, 1, -1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, 1, -1, -1, 1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, 1, -1, -1, 1, -1, 1, -1, -1, -1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1 -1 -1]
        self.pn5 = pn5 = [1,-1,1,-1,1, 1, 1, -1, 1, 1, -1, -1, -1, 1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, -1, 1, -1, -1, -1, -1]
        self.pi = pi = np.pi
        self.pfb_filter = pfb_filter = firdes.root_raised_cosine(nfilts_pfb, nfilts_pfb*sps, 1, rolloff, nfilts_pfb*11*sps+1)
        self.mark_delay = mark_delay = mark_delays[sps]
        self.header_formatter_0 = header_formatter_0 = digital.packet_header_default(header_len, len_tag_key,num_tag_key,1)
        self.header_formatter = header_formatter = digital.packet_header_default(header_len, len_tag_key,num_tag_key,1)
        self.const = const = digital.constellation_calcdist(digital.psk_2()[0], digital.psk_2()[1],
        2, 1).base()

        ##################################################
        # Blocks
        ##################################################
        self._snr_db_range = Range(0, 20, 0.5, snr_default, 200)
        self._snr_db_win = RangeWidget(self._snr_db_range, self.set_snr_db, 'SNR (dB)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._snr_db_win)
        self.wes_packet_tx_0 = wes_packet_tx(
            cw_len=cw_len,
            payload_len=payload_len,
            samp_rate=samp_rate,
        )
        self.qtgui_number_sink_0_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            1
        )
        self.qtgui_number_sink_0_0.set_update_time(0.10)
        self.qtgui_number_sink_0_0.set_title("# of Errors")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0_0.set_min(i, 0)
            self.qtgui_number_sink_0_0.set_max(i, 1e6)
            self.qtgui_number_sink_0_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_0.enable_autoscale(False)
        self._qtgui_number_sink_0_0_win = sip.wrapinstance(self.qtgui_number_sink_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_0_win)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            1
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("Bit Error Rate")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, -1)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "", #name
            2 #number of inputs
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(True)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 1, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, -1, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 0.5, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_win)
        self.pulse_shape_hier_0 = pulse_shape_hier(
            bFilter=1,
            roll_off=rolloff,
            sps=sps,
        )
        self.iio_pluto_source_0 = iio.pluto_source(epy_module_0.RX, int(900e6), int(samp_rate*1e3), 20000000, 32768, True, True, True, 'manual', 36, '', True)
        self.iio_pluto_sink_0 = iio.pluto_sink(epy_module_0.TX, int(900e6), int(samp_rate*1e3), 20000000, 32768, False, 10.0, '', True)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(sps, 2*pi/200, pfb_filter, nfilts_pfb, int(nfilts_pfb/2), 0.5, 1)
        self.digital_packet_headerparser_b_0_0 = digital.packet_headerparser_b(header_formatter.formatter())
        self.digital_header_payload_demux_0 = digital.header_payload_demux(
            header_len,
            1,
            0,
            "packet_length",
            "corr_est",
            False,
            gr.sizeof_gr_complex,
            "rx_time",
            1,
            (),
            0)
        self.digital_glfsr_source_x_0 = digital.glfsr_source_b(int(pn_order), True, 0, 1)
        self.digital_diff_decoder_bb_0_0 = digital.diff_decoder_bb(2)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(2)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(2*pi/200, 2, False)
        self.digital_corr_est_cc_0 = digital.corr_est_cc(pn6_padded, 1, 64, 0.8, digital.THRESHOLD_ABSOLUTE)
        self.digital_constellation_decoder_cb_0_0_0_0_0 = digital.constellation_decoder_cb(const)
        self.digital_constellation_decoder_cb_0_0_0_0 = digital.constellation_decoder_cb(const)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(const)
        self.digital_chunks_to_symbols_xx_0_0_0_0 = digital.chunks_to_symbols_bc((-1,1), 1)
        self.digital_chunks_to_symbols_xx_0_0_0 = digital.chunks_to_symbols_bc((-1,1), 1)
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc((-1,1), 1)
        self.calc_ber_0 = calc_ber()
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, np.sqrt(2)*np.sqrt(0.5 / np.power(10,snr_db/10)), 0)
        self.analog_agc_xx_0 = analog.agc_cc(1e-4, 1.0, 1.0)
        self.analog_agc_xx_0.set_max_gain(65536)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.digital_packet_headerparser_b_0_0, 'header_data'), (self.digital_header_payload_demux_0, 'header_data'))
        self.connect((self.analog_agc_xx_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_const_sink_x_0, 1))
        self.connect((self.calc_ber_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.calc_ber_0, 1), (self.qtgui_number_sink_0_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.calc_ber_0, 1))
        self.connect((self.digital_chunks_to_symbols_xx_0_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.digital_chunks_to_symbols_xx_0_0_0_0, 0), (self.calc_ber_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_chunks_to_symbols_xx_0_0_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0_0_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0_0_0_0, 0), (self.digital_diff_decoder_bb_0_0, 0))
        self.connect((self.digital_corr_est_cc_0, 0), (self.digital_header_payload_demux_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.digital_packet_headerparser_b_0_0, 0))
        self.connect((self.digital_diff_decoder_bb_0_0, 0), (self.digital_chunks_to_symbols_xx_0_0_0, 0))
        self.connect((self.digital_glfsr_source_x_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.digital_glfsr_source_x_0, 0), (self.wes_packet_tx_0, 0))
        self.connect((self.digital_header_payload_demux_0, 0), (self.digital_constellation_decoder_cb_0_0_0_0, 0))
        self.connect((self.digital_header_payload_demux_0, 1), (self.digital_constellation_decoder_cb_0_0_0_0_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_corr_est_cc_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.pulse_shape_hier_0, 0), (self.iio_pluto_sink_0, 0))
        self.connect((self.wes_packet_tx_0, 0), (self.pulse_shape_hier_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "lab3_ber")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_corr_tag_delay(self):
        return self.corr_tag_delay

    def set_corr_tag_delay(self, corr_tag_delay):
        self.corr_tag_delay = corr_tag_delay

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_mark_delay(self.mark_delays[self.sps])
        self.set_pfb_filter(firdes.root_raised_cosine(self.nfilts_pfb, self.nfilts_pfb*self.sps, 1, self.rolloff, self.nfilts_pfb*11*self.sps+1))
        self.set_rrc_filter(firdes.root_raised_cosine(4, self.sps, 1, self.rolloff, 32*self.sps+1))
        self.pulse_shape_hier_0.set_sps(self.sps)

    def get_snr_default(self):
        return self.snr_default

    def set_snr_default(self, snr_default):
        self.snr_default = snr_default
        self.set_snr_db(self.snr_default)

    def get_rolloff(self):
        return self.rolloff

    def set_rolloff(self, rolloff):
        self.rolloff = rolloff
        self.set_pfb_filter(firdes.root_raised_cosine(self.nfilts_pfb, self.nfilts_pfb*self.sps, 1, self.rolloff, self.nfilts_pfb*11*self.sps+1))
        self.set_rrc_filter(firdes.root_raised_cosine(4, self.sps, 1, self.rolloff, 32*self.sps+1))
        self.pulse_shape_hier_0.set_roll_off(self.rolloff)

    def get_payload_len(self):
        return self.payload_len

    def set_payload_len(self, payload_len):
        self.payload_len = payload_len
        self.set_pn_order(np.round(np.log2(self.payload_len+1)))
        self.set_tag_s(gr.tag_utils.python_to_tag((0, pmt.intern(self.len_tag_key), pmt.from_long(self.payload_len), pmt.intern("vect_test_src"))))
        self.wes_packet_tx_0.set_payload_len(self.payload_len)

    def get_num_tag_key(self):
        return self.num_tag_key

    def set_num_tag_key(self, num_tag_key):
        self.num_tag_key = num_tag_key
        self.set_header_formatter(digital.packet_header_default(self.header_len, self.len_tag_key,self.num_tag_key,1))
        self.set_header_formatter_0(digital.packet_header_default(self.header_len, self.len_tag_key,self.num_tag_key,1))

    def get_nfilts_pfb(self):
        return self.nfilts_pfb

    def set_nfilts_pfb(self, nfilts_pfb):
        self.nfilts_pfb = nfilts_pfb
        self.set_pfb_filter(firdes.root_raised_cosine(self.nfilts_pfb, self.nfilts_pfb*self.sps, 1, self.rolloff, self.nfilts_pfb*11*self.sps+1))

    def get_mark_delays(self):
        return self.mark_delays

    def set_mark_delays(self, mark_delays):
        self.mark_delays = mark_delays
        self.set_mark_delay(self.mark_delays[self.sps])

    def get_len_tag_key(self):
        return self.len_tag_key

    def set_len_tag_key(self, len_tag_key):
        self.len_tag_key = len_tag_key
        self.set_header_formatter(digital.packet_header_default(self.header_len, self.len_tag_key,self.num_tag_key,1))
        self.set_header_formatter_0(digital.packet_header_default(self.header_len, self.len_tag_key,self.num_tag_key,1))
        self.set_tag0(gr.tag_utils.python_to_tag((0, pmt.intern(self.len_tag_key), pmt.from_long(self.cw_len), pmt.intern("vect_cw_src"))))
        self.set_tag_s(gr.tag_utils.python_to_tag((0, pmt.intern(self.len_tag_key), pmt.from_long(self.payload_len), pmt.intern("vect_test_src"))))

    def get_header_len(self):
        return self.header_len

    def set_header_len(self, header_len):
        self.header_len = header_len
        self.set_header_formatter(digital.packet_header_default(self.header_len, self.len_tag_key,self.num_tag_key,1))
        self.set_header_formatter_0(digital.packet_header_default(self.header_len, self.len_tag_key,self.num_tag_key,1))

    def get_cw_len(self):
        return self.cw_len

    def set_cw_len(self, cw_len):
        self.cw_len = cw_len
        self.set_tag0(gr.tag_utils.python_to_tag((0, pmt.intern(self.len_tag_key), pmt.from_long(self.cw_len), pmt.intern("vect_cw_src"))))
        self.wes_packet_tx_0.set_cw_len(self.cw_len)

    def get_tag_s(self):
        return self.tag_s

    def set_tag_s(self, tag_s):
        self.tag_s = tag_s

    def get_tag0(self):
        return self.tag0

    def set_tag0(self, tag0):
        self.tag0 = tag0

    def get_sync_seq(self):
        return self.sync_seq

    def set_sync_seq(self, sync_seq):
        self.sync_seq = sync_seq

    def get_snr_db(self):
        return self.snr_db

    def set_snr_db(self, snr_db):
        self.snr_db = snr_db
        self.analog_noise_source_x_0.set_amplitude(np.sqrt(2)*np.sqrt(0.5 / np.power(10,self.snr_db/10)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.iio_pluto_sink_0.set_params(int(900e6), int(self.samp_rate*1e3), 20000000, 10.0, '', True)
        self.iio_pluto_source_0.set_params(int(900e6), int(self.samp_rate*1e3), 20000000, True, True, True, 'manual', 36, '', True)
        self.wes_packet_tx_0.set_samp_rate(self.samp_rate)

    def get_rrc_filter(self):
        return self.rrc_filter

    def set_rrc_filter(self, rrc_filter):
        self.rrc_filter = rrc_filter

    def get_pn_order(self):
        return self.pn_order

    def set_pn_order(self, pn_order):
        self.pn_order = pn_order

    def get_pn6_padded(self):
        return self.pn6_padded

    def set_pn6_padded(self, pn6_padded):
        self.pn6_padded = pn6_padded

    def get_pn6(self):
        return self.pn6

    def set_pn6(self, pn6):
        self.pn6 = pn6

    def get_pn5(self):
        return self.pn5

    def set_pn5(self, pn5):
        self.pn5 = pn5

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

    def get_mark_delay(self):
        return self.mark_delay

    def set_mark_delay(self, mark_delay):
        self.mark_delay = mark_delay

    def get_header_formatter_0(self):
        return self.header_formatter_0

    def set_header_formatter_0(self, header_formatter_0):
        self.header_formatter_0 = header_formatter_0

    def get_header_formatter(self):
        return self.header_formatter

    def set_header_formatter(self, header_formatter):
        self.header_formatter = header_formatter

    def get_const(self):
        return self.const

    def set_const(self, const):
        self.const = const


def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-c", "--corr-tag-delay", dest="corr_tag_delay", type=intx, default=131,
        help="Set Correlation Tag Delay [default=%(default)r]")
    return parser


def main(top_block_cls=lab3_ber, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(corr_tag_delay=options.corr_tag_delay)
    tb.start()
    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()