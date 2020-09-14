#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: BER Example
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
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from wes_packet_tx import wes_packet_tx  # grc-generated hier_block
import numpy as np
import pmt
from gnuradio import qtgui

class ber_test(gr.top_block, Qt.QWidget):

    def __init__(self, corr_tag_delay=131, eb=0.5):
        gr.top_block.__init__(self, "BER Example")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("BER Example")
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

        self.settings = Qt.QSettings("GNU Radio", "ber_test")

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
        self.eb = eb

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 1
        self.payload_len = payload_len = 31
        self.num_tag_key = num_tag_key = "packet_num"
        self.mark_delays = mark_delays = [0, 0, 34, 56, 87, 119]
        self.len_tag_key = len_tag_key = "packet_length"
        self.header_len = header_len = 32
        self.cw_len = cw_len = 32
        self.tag_s = tag_s = gr.tag_utils.python_to_tag((0, pmt.intern(len_tag_key), pmt.from_long(payload_len), pmt.intern("vect_test_src")))
        self.tag_delay = tag_delay = 64
        self.tag0 = tag0 = gr.tag_utils.python_to_tag((0, pmt.intern(len_tag_key), pmt.from_long(cw_len), pmt.intern("vect_cw_src")))
        self.sync_seq = sync_seq = [1, 1, -1, 1, -1, 1, 1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1, 1, 1, -1, 1, 1, -1, -1, -1, -1, 1, 1, -1, -1, 1, 1, 1, -1, -1, 1, 1, 1, -1, -1, 1, -1, -1, 1, -1, 1, -1, 1, -1, -1, -1, 1, -1, 1, 1, -1, -1, -1, 1, 1, 1, 1, 1, 1]
        self.sigma = sigma = 0.2
        self.samp_rate = samp_rate = 1e3
        self.rolloff = rolloff = 0.5
        self.pn_order = pn_order = np.round(np.log2(payload_len+1))
        self.pn6_padded = pn6_padded = [1, 1, 1, 1, 1, 1, -1, 1, -1, 1, -1, 1, 1, -1, -1, 1, 1, -1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, 1, -1, -1, 1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, 1, -1, -1, 1, -1, 1, -1, -1, -1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1 -1 -1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.pn6 = pn6 = [1, 1, 1, 1, 1, 1, -1, 1, -1, 1, -1, 1, 1, -1, -1, 1, 1, -1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, 1, -1, -1, 1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, 1, -1, -1, 1, -1, 1, -1, -1, -1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1 -1 -1]
        self.pn5 = pn5 = [1,-1,1,-1,1, 1, 1, -1, 1, 1, -1, -1, -1, 1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, -1, 1, -1, -1, -1, -1]
        self.mark_delay = mark_delay = mark_delays[sps]
        self.header_formatter_0 = header_formatter_0 = digital.packet_header_default(header_len, len_tag_key,num_tag_key,1)
        self.header_formatter = header_formatter = digital.packet_header_default(header_len, len_tag_key,num_tag_key,1)
        self.const = const = digital.constellation_calcdist(digital.psk_2()[0], digital.psk_2()[1],
        2, 1).base()

        ##################################################
        # Blocks
        ##################################################
        self._tag_delay_range = Range(0, 131, 1, 64, 200)
        self._tag_delay_win = RangeWidget(self._tag_delay_range, self.set_tag_delay, 'Tag Marking Delay', "counter_slider", float)
        self.top_grid_layout.addWidget(self._tag_delay_win)
        self.wes_packet_tx_0 = wes_packet_tx(
            cw_len=cw_len,
            payload_len=payload_len,
            samp_rate=samp_rate,
        )
        self._sigma_range = Range(0, 1, 0.001, 0.2, 200)
        self._sigma_win = RangeWidget(self._sigma_range, self.set_sigma, 'Std. Dev.', "counter_slider", float)
        self.top_grid_layout.addWidget(self._sigma_win)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
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
        self.iir_filter_xxx_0_0 = filter.iir_filter_ffd([1], [1, 1], True)
        self.iir_filter_xxx_0 = filter.iir_filter_ffd([1], [1, 1], True)
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
        self.digital_corr_est_cc_0 = digital.corr_est_cc(pn6_padded, sps, tag_delay, 0.8, digital.THRESHOLD_ABSOLUTE)
        self.digital_constellation_decoder_cb_0_0_0_0 = digital.constellation_decoder_cb(const)
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc((-1,1), 1)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
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
        self.msg_connect((self.digital_packet_headerparser_b_0_0, 'header_data'), (self.digital_header_payload_demux_0, 'header_data'))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_complex_to_mag_0_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.iir_filter_xxx_0, 0))
        self.connect((self.blocks_complex_to_mag_0_0, 0), (self.iir_filter_xxx_0_0, 0))
        self.connect((self.blocks_divide_xx_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.blocks_max_xx_0, 0), (self.blocks_divide_xx_0, 1))
        self.connect((self.blocks_max_xx_0_0, 0), (self.blocks_divide_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.digital_header_payload_demux_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.digital_constellation_decoder_cb_0_0_0_0, 0), (self.digital_packet_headerparser_b_0_0, 0))
        self.connect((self.digital_corr_est_cc_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.digital_glfsr_source_x_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.digital_glfsr_source_x_0, 0), (self.wes_packet_tx_0, 0))
        self.connect((self.digital_header_payload_demux_0, 1), (self.blocks_sub_xx_0, 0))
        self.connect((self.digital_header_payload_demux_0, 0), (self.digital_constellation_decoder_cb_0_0_0_0, 0))
        self.connect((self.iir_filter_xxx_0, 0), (self.blocks_max_xx_0_0, 0))
        self.connect((self.iir_filter_xxx_0_0, 0), (self.blocks_max_xx_0, 0))
        self.connect((self.wes_packet_tx_0, 0), (self.digital_corr_est_cc_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ber_test")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_corr_tag_delay(self):
        return self.corr_tag_delay

    def set_corr_tag_delay(self, corr_tag_delay):
        self.corr_tag_delay = corr_tag_delay

    def get_eb(self):
        return self.eb

    def set_eb(self, eb):
        self.eb = eb

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_mark_delay(self.mark_delays[self.sps])

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

    def get_tag_delay(self):
        return self.tag_delay

    def set_tag_delay(self, tag_delay):
        self.tag_delay = tag_delay
        self.digital_corr_est_cc_0.set_mark_delay(self.tag_delay)

    def get_tag0(self):
        return self.tag0

    def set_tag0(self, tag0):
        self.tag0 = tag0

    def get_sync_seq(self):
        return self.sync_seq

    def set_sync_seq(self, sync_seq):
        self.sync_seq = sync_seq

    def get_sigma(self):
        return self.sigma

    def set_sigma(self, sigma):
        self.sigma = sigma

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.wes_packet_tx_0.set_samp_rate(self.samp_rate)

    def get_rolloff(self):
        return self.rolloff

    def set_rolloff(self, rolloff):
        self.rolloff = rolloff

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
    parser.add_argument(
        "--eb", dest="eb", type=eng_float, default="500.0m",
        help="Set Filter Rolloff [default=%(default)r]")
    return parser


def main(top_block_cls=ber_test, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(corr_tag_delay=options.corr_tag_delay, eb=options.eb)
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
