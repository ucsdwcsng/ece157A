#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Lab 4
# Author: wes
# GNU Radio version: 3.8.2.0

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

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from math import pi
from scipy import signal as sp
import iio
import numpy as np
import random as rand

from gnuradio import qtgui

class lab4_random(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Lab 4")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Lab 4")
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

        self.settings = Qt.QSettings("GNU Radio", "lab4_random")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.echo_gain_iir = echo_gain_iir = 0
        self.delay_limit = delay_limit = 64
        self.delay_iir = delay_iir = 1
        self.sps = sps = 4
        self.pn6 = pn6 = [1, 1, 1, 1, 1, 1, -1, 1, -1, 1, -1, 1, 1, -1, -1, 1, 1, -1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, 1, -1, -1, 1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, 1, -1, -1, 1, -1, 1, -1, -1, -1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1 -1 -1]
        self.pn5 = pn5 = [1,-1,1,-1,1, 1, 1, -1, 1, 1, -1, -1, -1, 1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, -1, 1, -1, -1, -1, -1]
        self.iir_taps_2 = iir_taps_2 = np.concatenate( ([1], np.zeros(int(delay_iir-1)),[-echo_gain_iir],np.zeros(int(delay_limit-delay_iir)))     )
        self.h_filt = h_filt = [1,1,1,1]
        self.freqc = freqc = 900
        self.samp_rate = samp_rate = 1000
        self.pn6_up = pn6_up = sp.upfirdn( h_filt, pn6, sps )
        self.pn5_up = pn5_up = sp.upfirdn( h_filt, pn5, sps )
        self.phase_shift = phase_shift = 1
        self.lw = lw = 2
        self.iir_taps = iir_taps = iir_taps_2
        self.gain_ = gain_ = 0.5
        self.freqc_ = freqc_ = freqc
        self.fps = fps = 30
        self.fo = fo = 800
        self.equalize_on = equalize_on = 0
        self.echo_gain = echo_gain = rand.uniform(0.2,0.9)
        self.delay = delay = rand.randint(10,delay_limit-10)
        self.const_qpsk = const_qpsk = digital.constellation_calcdist(digital.psk_4()[0], digital.psk_4()[1],
        4, 1).base()
        self.const_bpsk = const_bpsk = digital.constellation_calcdist(digital.psk_2()[0], digital.psk_2()[1],
        2, 1).base()
        self.bw = bw = 1
        self.buff_size = buff_size = 32768
        self.axis = axis = 2
        self.PLL_ON = PLL_ON = 0

        ##################################################
        # Blocks
        ##################################################
        self.tab0 = Qt.QTabWidget()
        self.tab0_widget_0 = Qt.QWidget()
        self.tab0_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab0_widget_0)
        self.tab0_grid_layout_0 = Qt.QGridLayout()
        self.tab0_layout_0.addLayout(self.tab0_grid_layout_0)
        self.tab0.addTab(self.tab0_widget_0, 'Cross-Correlation')
        self.tab0_widget_1 = Qt.QWidget()
        self.tab0_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab0_widget_1)
        self.tab0_grid_layout_1 = Qt.QGridLayout()
        self.tab0_layout_1.addLayout(self.tab0_grid_layout_1)
        self.tab0.addTab(self.tab0_widget_1, 'Spectrum')
        self.top_grid_layout.addWidget(self.tab0, 0, 0, 10, 2)
        for r in range(0, 10):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        _phase_shift_check_box = Qt.QCheckBox('PI Phase Shift')
        self._phase_shift_choices = {True: 1, False: 0}
        self._phase_shift_choices_inv = dict((v,k) for k,v in self._phase_shift_choices.items())
        self._phase_shift_callback = lambda i: Qt.QMetaObject.invokeMethod(_phase_shift_check_box, "setChecked", Qt.Q_ARG("bool", self._phase_shift_choices_inv[i]))
        self._phase_shift_callback(self.phase_shift)
        _phase_shift_check_box.stateChanged.connect(lambda i: self.set_phase_shift(self._phase_shift_choices[bool(i)]))
        self.top_grid_layout.addWidget(_phase_shift_check_box, 12, 1, 1, 1)
        for r in range(12, 13):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._gain__range = Range(0.1, 1, 0.01, 0.5, 200)
        self._gain__win = RangeWidget(self._gain__range, self.set_gain_, 'Gain (Amp)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._gain__win, 10, 1, 1, 1)
        for r in range(10, 11):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freqc__range = Range(70, 6000, .01, freqc, 200)
        self._freqc__win = RangeWidget(self._freqc__range, self.set_freqc_, 'Carrier (MHz)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._freqc__win, 10, 0, 1, 1)
        for r in range(10, 11):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._fo_range = Range(-10000, 10000, 1, 800, 200)
        self._fo_win = RangeWidget(self._fo_range, self.set_fo, 'Frequency Offset (Hz)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._fo_win, 12, 0, 1, 1)
        for r in range(12, 13):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._equalize_on_options = (0, 1, )
        # Create the labels list
        self._equalize_on_labels = ('Equalizer Off', 'Equalizer On', )
        # Create the combo box
        self._equalize_on_tool_bar = Qt.QToolBar(self)
        self._equalize_on_tool_bar.addWidget(Qt.QLabel('Equalizer Select' + ": "))
        self._equalize_on_combo_box = Qt.QComboBox()
        self._equalize_on_tool_bar.addWidget(self._equalize_on_combo_box)
        for _label in self._equalize_on_labels: self._equalize_on_combo_box.addItem(_label)
        self._equalize_on_callback = lambda i: Qt.QMetaObject.invokeMethod(self._equalize_on_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._equalize_on_options.index(i)))
        self._equalize_on_callback(self.equalize_on)
        self._equalize_on_combo_box.currentIndexChanged.connect(
            lambda i: self.set_equalize_on(self._equalize_on_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._equalize_on_tool_bar, 13, 0, 1, 1)
        for r in range(13, 14):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._PLL_ON_options = (0, 1, )
        # Create the labels list
        self._PLL_ON_labels = ('PLL ON', 'PLL OFF', )
        # Create the combo box
        self._PLL_ON_tool_bar = Qt.QToolBar(self)
        self._PLL_ON_tool_bar.addWidget(Qt.QLabel('PLL Select' + ": "))
        self._PLL_ON_combo_box = Qt.QComboBox()
        self._PLL_ON_tool_bar.addWidget(self._PLL_ON_combo_box)
        for _label in self._PLL_ON_labels: self._PLL_ON_combo_box.addItem(_label)
        self._PLL_ON_callback = lambda i: Qt.QMetaObject.invokeMethod(self._PLL_ON_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._PLL_ON_options.index(i)))
        self._PLL_ON_callback(self.PLL_ON)
        self._PLL_ON_combo_box.currentIndexChanged.connect(
            lambda i: self.set_PLL_ON(self._PLL_ON_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._PLL_ON_tool_bar, 13, 1, 1, 1)
        for r in range(13, 14):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
            4096, #size
            samp_rate*1000, #samp_rate
            "Cross Correlation", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.tab0_grid_layout_0.addWidget(self._qtgui_time_sink_x_0_0_win, 5, 0, 5, 1)
        for r in range(5, 10):
            self.tab0_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tab0_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            4096, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate*1e3, #bw
            "", #name
            1
        )
        self.qtgui_freq_sink_x_0.set_update_time(1/fps)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(True)



        labels = ['In-Phase', 'Quadrature', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab0_grid_layout_1.addWidget(self._qtgui_freq_sink_x_0_win, 5, 0, 5, 1)
        for r in range(5, 10):
            self.tab0_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tab0_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0.set_processor_affinity([0])
        self.interp_fir_filter_xxx_1_0 = filter.interp_fir_filter_ccc(sps, (1,1,1,1))
        self.interp_fir_filter_xxx_1_0.declare_sample_delay(0)
        self.iir_filter_xxx_0 = filter.iir_filter_ccz([(1)], iir_taps, True)
        self.iio_pluto_source_0 = iio.pluto_source('', int(freqc_*1e6), int(samp_rate*1000), 20000000, buff_size, True, True, True, 'manual', 32, '', True)
        self.iio_pluto_sink_0 = iio.pluto_sink('', int(freqc_*1e6), int(samp_rate*1000), 20000000, buff_size, False, 10.0, '', True)
        self._echo_gain_iir_range = Range(0, 1, 0.01, 0, 200)
        self._echo_gain_iir_win = RangeWidget(self._echo_gain_iir_range, self.set_echo_gain_iir, 'Equalizer Gain (A)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._echo_gain_iir_win, 14, 0, 1, 1)
        for r in range(14, 15):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.digital_glfsr_source_x_0 = digital.glfsr_source_b(6, True, 0, 1)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(3.14/100, 2, False)
        self.digital_corr_est_cc_0 = digital.corr_est_cc(pn6_up, sps, 0, 0.7, digital.THRESHOLD_ABSOLUTE)
        self.digital_chunks_to_symbols_xx_1 = digital.chunks_to_symbols_bc(const_bpsk.points(), 1)
        self._delay_iir_range = Range(1, delay_limit, 1, 1, 200)
        self._delay_iir_win = RangeWidget(self._delay_iir_range, self.set_delay_iir, 'Equalizer Delay (samples)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._delay_iir_win, 14, 1, 1, 1)
        for r in range(14, 15):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_tag_gate_0_0_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_tag_gate_0_0_0.set_single_key("time_est")
        self.blocks_tag_gate_0_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_tag_gate_0_0.set_single_key("corr_est")
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_tag_gate_0.set_single_key("amp_est")
        self.blocks_selector_0_0 = blocks.selector(gr.sizeof_gr_complex*1,equalize_on,0)
        self.blocks_selector_0_0.set_enabled(True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,PLL_ON,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_2 = blocks.multiply_const_cc((1/63/sps)*np.exp(1j*pi*phase_shift))
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_cc(echo_gain)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(gain_ )
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, delay)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate*1000, analog.GR_COS_WAVE, fo, 1, 0, 0)
        self.analog_agc_xx_0 = analog.agc_cc(1e-4, 1.0, 1.0)
        self.analog_agc_xx_0.set_max_gain(65536)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc_xx_0, 0), (self.blocks_selector_0, 1))
        self.connect((self.analog_agc_xx_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_2, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.iio_pluto_sink_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.blocks_selector_0_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.iir_filter_xxx_0, 0))
        self.connect((self.blocks_selector_0_0, 0), (self.digital_corr_est_cc_0, 0))
        self.connect((self.blocks_selector_0_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.blocks_tag_gate_0_0, 0))
        self.connect((self.blocks_tag_gate_0_0, 0), (self.blocks_tag_gate_0_0_0, 0))
        self.connect((self.blocks_tag_gate_0_0_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_1, 0), (self.interp_fir_filter_xxx_1_0, 0))
        self.connect((self.digital_corr_est_cc_0, 1), (self.blocks_multiply_const_vxx_2, 0))
        self.connect((self.digital_corr_est_cc_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.digital_glfsr_source_x_0, 0), (self.digital_chunks_to_symbols_xx_1, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.iir_filter_xxx_0, 0), (self.blocks_selector_0_0, 1))
        self.connect((self.interp_fir_filter_xxx_1_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.interp_fir_filter_xxx_1_0, 0), (self.blocks_delay_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "lab4_random")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_echo_gain_iir(self):
        return self.echo_gain_iir

    def set_echo_gain_iir(self, echo_gain_iir):
        self.echo_gain_iir = echo_gain_iir
        self.set_iir_taps_2(np.concatenate( ([1], np.zeros(int(self.delay_iir-1)),[-self.echo_gain_iir],np.zeros(int(self.delay_limit-self.delay_iir)))     ))

    def get_delay_limit(self):
        return self.delay_limit

    def set_delay_limit(self, delay_limit):
        self.delay_limit = delay_limit
        self.set_delay(rand.randint(10,self.delay_limit-10))
        self.set_iir_taps_2(np.concatenate( ([1], np.zeros(int(self.delay_iir-1)),[-self.echo_gain_iir],np.zeros(int(self.delay_limit-self.delay_iir)))     ))

    def get_delay_iir(self):
        return self.delay_iir

    def set_delay_iir(self, delay_iir):
        self.delay_iir = delay_iir
        self.set_iir_taps_2(np.concatenate( ([1], np.zeros(int(self.delay_iir-1)),[-self.echo_gain_iir],np.zeros(int(self.delay_limit-self.delay_iir)))     ))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_pn5_up(sp.upfirdn( self.h_filt, self.pn5, self.sps ))
        self.set_pn6_up(sp.upfirdn( self.h_filt, self.pn6, self.sps ))
        self.blocks_multiply_const_vxx_2.set_k((1/63/self.sps)*np.exp(1j*pi*self.phase_shift))

    def get_pn6(self):
        return self.pn6

    def set_pn6(self, pn6):
        self.pn6 = pn6
        self.set_pn6_up(sp.upfirdn( self.h_filt, self.pn6, self.sps ))

    def get_pn5(self):
        return self.pn5

    def set_pn5(self, pn5):
        self.pn5 = pn5
        self.set_pn5_up(sp.upfirdn( self.h_filt, self.pn5, self.sps ))

    def get_iir_taps_2(self):
        return self.iir_taps_2

    def set_iir_taps_2(self, iir_taps_2):
        self.iir_taps_2 = iir_taps_2
        self.set_iir_taps(self.iir_taps_2)

    def get_h_filt(self):
        return self.h_filt

    def set_h_filt(self, h_filt):
        self.h_filt = h_filt
        self.set_pn5_up(sp.upfirdn( self.h_filt, self.pn5, self.sps ))
        self.set_pn6_up(sp.upfirdn( self.h_filt, self.pn6, self.sps ))

    def get_freqc(self):
        return self.freqc

    def set_freqc(self, freqc):
        self.freqc = freqc
        self.set_freqc_(self.freqc)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate*1000)
        self.iio_pluto_sink_0.set_params(int(self.freqc_*1e6), int(self.samp_rate*1000), 20000000, 10.0, '', True)
        self.iio_pluto_source_0.set_params(int(self.freqc_*1e6), int(self.samp_rate*1000), 20000000, True, True, True, 'manual', 32, '', True)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate*1e3)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate*1000)

    def get_pn6_up(self):
        return self.pn6_up

    def set_pn6_up(self, pn6_up):
        self.pn6_up = pn6_up

    def get_pn5_up(self):
        return self.pn5_up

    def set_pn5_up(self, pn5_up):
        self.pn5_up = pn5_up

    def get_phase_shift(self):
        return self.phase_shift

    def set_phase_shift(self, phase_shift):
        self.phase_shift = phase_shift
        self._phase_shift_callback(self.phase_shift)
        self.blocks_multiply_const_vxx_2.set_k((1/63/self.sps)*np.exp(1j*pi*self.phase_shift))

    def get_lw(self):
        return self.lw

    def set_lw(self, lw):
        self.lw = lw

    def get_iir_taps(self):
        return self.iir_taps

    def set_iir_taps(self, iir_taps):
        self.iir_taps = iir_taps
        self.iir_filter_xxx_0.set_taps([(1)], self.iir_taps)

    def get_gain_(self):
        return self.gain_

    def set_gain_(self, gain_):
        self.gain_ = gain_
        self.blocks_multiply_const_vxx_0.set_k(self.gain_ )

    def get_freqc_(self):
        return self.freqc_

    def set_freqc_(self, freqc_):
        self.freqc_ = freqc_
        self.iio_pluto_sink_0.set_params(int(self.freqc_*1e6), int(self.samp_rate*1000), 20000000, 10.0, '', True)
        self.iio_pluto_source_0.set_params(int(self.freqc_*1e6), int(self.samp_rate*1000), 20000000, True, True, True, 'manual', 32, '', True)

    def get_fps(self):
        return self.fps

    def set_fps(self, fps):
        self.fps = fps
        self.qtgui_freq_sink_x_0.set_update_time(1/self.fps)

    def get_fo(self):
        return self.fo

    def set_fo(self, fo):
        self.fo = fo
        self.analog_sig_source_x_0.set_frequency(self.fo)

    def get_equalize_on(self):
        return self.equalize_on

    def set_equalize_on(self, equalize_on):
        self.equalize_on = equalize_on
        self._equalize_on_callback(self.equalize_on)
        self.blocks_selector_0_0.set_input_index(self.equalize_on)

    def get_echo_gain(self):
        return self.echo_gain

    def set_echo_gain(self, echo_gain):
        self.echo_gain = echo_gain
        self.blocks_multiply_const_vxx_1.set_k(self.echo_gain)

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay
        self.blocks_delay_0.set_dly(self.delay)

    def get_const_qpsk(self):
        return self.const_qpsk

    def set_const_qpsk(self, const_qpsk):
        self.const_qpsk = const_qpsk

    def get_const_bpsk(self):
        return self.const_bpsk

    def set_const_bpsk(self, const_bpsk):
        self.const_bpsk = const_bpsk

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw

    def get_buff_size(self):
        return self.buff_size

    def set_buff_size(self, buff_size):
        self.buff_size = buff_size

    def get_axis(self):
        return self.axis

    def set_axis(self, axis):
        self.axis = axis

    def get_PLL_ON(self):
        return self.PLL_ON

    def set_PLL_ON(self, PLL_ON):
        self.PLL_ON = PLL_ON
        self._PLL_ON_callback(self.PLL_ON)
        self.blocks_selector_0.set_input_index(self.PLL_ON)





def main(top_block_cls=lab4_random, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

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
