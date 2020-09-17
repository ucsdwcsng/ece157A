#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Lab 3
# Author: wes
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

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
import numpy
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
import epy_module_0  # embedded python module
import iio
import numpy as np
import wes
from gnuradio import qtgui

class lab3(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Lab 3")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Lab 3")
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

        self.settings = Qt.QSettings("GNU Radio", "lab3")

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
        self.freqc = freqc = 900
        self.zeta = zeta = 0.707
        self.std_dev = std_dev = 0.01
        self.sps = sps = 8
        self.samp_rate = samp_rate = 1000
        self.nat_freq = nat_freq = 10000
        self.lw = lw = 2
        self.gain_ = gain_ = 0.5
        self.freqc_ = freqc_ = freqc
        self.fps = fps = 30
        self.fo = fo = 0
        self.const_qpsk = const_qpsk = digital.constellation_calcdist(digital.psk_4()[0], digital.psk_4()[1],
        4, 1).base()
        self.const_bpsk = const_bpsk = digital.constellation_calcdist(digital.psk_2()[0], digital.psk_2()[1],
        2, 1).base()
        self.bw = bw = 1
        self.buff_size = buff_size = 32768
        self.bSignal = bSignal = 0
        self.bSelectPLL = bSelectPLL = 0
        self.axis = axis = 2

        ##################################################
        # Blocks
        ##################################################
        self._zeta_range = Range(0, 4, 0.001, 0.707, 200)
        self._zeta_win = RangeWidget(self._zeta_range, self.set_zeta, 'Damping Factor (Zeta)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._zeta_win, 13, 0, 1, 1)
        for r in range(13, 14):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.tab0 = Qt.QTabWidget()
        self.tab0_widget_0 = Qt.QWidget()
        self.tab0_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab0_widget_0)
        self.tab0_grid_layout_0 = Qt.QGridLayout()
        self.tab0_layout_0.addLayout(self.tab0_grid_layout_0)
        self.tab0.addTab(self.tab0_widget_0, 'Loop Filter Output')
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
        self._std_dev_range = Range(0, 0.1, 0.001, 0.01, 200)
        self._std_dev_win = RangeWidget(self._std_dev_range, self.set_std_dev, 'Noise Std. Dev', "counter_slider", float)
        self.top_grid_layout.addWidget(self._std_dev_win, 11, 0, 1, 1)
        for r in range(11, 12):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._nat_freq_range = Range(0, 100e3, 1, 10000, 200)
        self._nat_freq_win = RangeWidget(self._nat_freq_range, self.set_nat_freq, 'Natural Freq (Hz)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._nat_freq_win, 13, 1, 1, 1)
        for r in range(13, 14):
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
        self._fo_range = Range(0, 100e3, 100, 0, 200)
        self._fo_win = RangeWidget(self._fo_range, self.set_fo, 'Frequency Offset (Hz)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._fo_win, 11, 1, 1, 1)
        for r in range(11, 12):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._bSignal_options = (0, 1, 2, )
        # Create the labels list
        self._bSignal_labels = ('Tone', 'BPSK', 'QPSK', )
        # Create the combo box
        # Create the radio buttons
        self._bSignal_group_box = Qt.QGroupBox('Signal Select' + ": ")
        self._bSignal_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._bSignal_button_group = variable_chooser_button_group()
        self._bSignal_group_box.setLayout(self._bSignal_box)
        for i, _label in enumerate(self._bSignal_labels):
            radio_button = Qt.QRadioButton(_label)
            self._bSignal_box.addWidget(radio_button)
            self._bSignal_button_group.addButton(radio_button, i)
        self._bSignal_callback = lambda i: Qt.QMetaObject.invokeMethod(self._bSignal_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._bSignal_options.index(i)))
        self._bSignal_callback(self.bSignal)
        self._bSignal_button_group.buttonClicked[int].connect(
            lambda i: self.set_bSignal(self._bSignal_options[i]))
        self.top_grid_layout.addWidget(self._bSignal_group_box, 12, 0, 1, 1)
        for r in range(12, 13):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._bSelectPLL_options = (0, 1, 2, 3, )
        # Create the labels list
        self._bSelectPLL_labels = ('Standard', 'Costas', 'Costas w/ HL', 'QPSK Costas', )
        # Create the combo box
        # Create the radio buttons
        self._bSelectPLL_group_box = Qt.QGroupBox('PLL Order' + ": ")
        self._bSelectPLL_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._bSelectPLL_button_group = variable_chooser_button_group()
        self._bSelectPLL_group_box.setLayout(self._bSelectPLL_box)
        for i, _label in enumerate(self._bSelectPLL_labels):
            radio_button = Qt.QRadioButton(_label)
            self._bSelectPLL_box.addWidget(radio_button)
            self._bSelectPLL_button_group.addButton(radio_button, i)
        self._bSelectPLL_callback = lambda i: Qt.QMetaObject.invokeMethod(self._bSelectPLL_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._bSelectPLL_options.index(i)))
        self._bSelectPLL_callback(self.bSelectPLL)
        self._bSelectPLL_button_group.buttonClicked[int].connect(
            lambda i: self.set_bSelectPLL(self._bSelectPLL_options[i]))
        self.top_grid_layout.addWidget(self._bSelectPLL_group_box, 12, 1, 1, 1)
        for r in range(12, 13):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.wes_costas_cc_0 = wes.costas_cc(nat_freq / (samp_rate*1000), zeta, bSelectPLL)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_c(
            4096, #size
            samp_rate, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-10000, 10000)

        self.qtgui_time_sink_x_0_0.set_y_label('Frequency (Hz)', "")

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


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
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
            1024, #size
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
        self.qtgui_freq_sink_x_0.enable_control_panel(False)



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
        self.interp_fir_filter_xxx_1_0_0 = filter.interp_fir_filter_ccc(sps, (1,1,1,1,1,1,1,1))
        self.interp_fir_filter_xxx_1_0_0.declare_sample_delay(0)
        self.interp_fir_filter_xxx_1_0 = filter.interp_fir_filter_ccc(sps, (1,1,1,1,1,1,1,1))
        self.interp_fir_filter_xxx_1_0.declare_sample_delay(0)
        self.iio_pluto_source_0 = iio.pluto_source(epy_module_0.RX, int(freqc_*1e6), int(samp_rate*1000), 20000000, buff_size, True, True, True, 'manual', 32, '', True)
        self.iio_pluto_sink_0 = iio.pluto_sink(epy_module_0.TX, int(freqc_*1e6), int(samp_rate*1000), 20000000, buff_size, False, 10.0, '', True)
        self.digital_chunks_to_symbols_xx_1_0 = digital.chunks_to_symbols_bc(const_qpsk.points(), 1)
        self.digital_chunks_to_symbols_xx_1 = digital.chunks_to_symbols_bc(const_bpsk.points(), 1)
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_selector_0_0 = blocks.selector(gr.sizeof_gr_complex*1,bSignal,0)
        self.blocks_selector_0_0.set_enabled(True)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_2 = blocks.multiply_const_cc(1/6.28*samp_rate*1000)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_cc(0)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(gain_ )
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_cc(1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate*1000, analog.GR_COS_WAVE, fo, 1, 0, 0)
        self.analog_random_source_x_0_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 4, 8192))), True)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 2, 8192))), True)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, std_dev, 0)
        self.analog_agc_xx_0 = analog.agc_cc(1e-4, 1.0, 1.0)
        self.analog_agc_xx_0.set_max_gain(65536)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc_xx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.analog_agc_xx_0, 0), (self.wes_costas_cc_0, 0))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_chunks_to_symbols_xx_1, 0))
        self.connect((self.analog_random_source_x_0_0, 0), (self.digital_chunks_to_symbols_xx_1_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_selector_0_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_2, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.iio_pluto_sink_0, 0))
        self.connect((self.blocks_selector_0_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.blocks_multiply_const_vxx_2, 0))
        self.connect((self.digital_chunks_to_symbols_xx_1, 0), (self.interp_fir_filter_xxx_1_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_1_0, 0), (self.interp_fir_filter_xxx_1_0_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.interp_fir_filter_xxx_1_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.interp_fir_filter_xxx_1_0, 0), (self.blocks_selector_0_0, 1))
        self.connect((self.interp_fir_filter_xxx_1_0_0, 0), (self.blocks_selector_0_0, 2))
        self.connect((self.wes_costas_cc_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.wes_costas_cc_0, 1), (self.blocks_tag_gate_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "lab3")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_freqc(self):
        return self.freqc

    def set_freqc(self, freqc):
        self.freqc = freqc
        self.set_freqc_(self.freqc)

    def get_zeta(self):
        return self.zeta

    def set_zeta(self, zeta):
        self.zeta = zeta
        self.wes_costas_cc_0.set_damping(self.zeta)

    def get_std_dev(self):
        return self.std_dev

    def set_std_dev(self, std_dev):
        self.std_dev = std_dev
        self.analog_noise_source_x_0.set_amplitude(self.std_dev)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate*1000)
        self.blocks_multiply_const_vxx_2.set_k(1/6.28*self.samp_rate*1000)
        self.iio_pluto_sink_0.set_params(int(self.freqc_*1e6), int(self.samp_rate*1000), 20000000, 10.0, '', True)
        self.iio_pluto_source_0.set_params(int(self.freqc_*1e6), int(self.samp_rate*1000), 20000000, True, True, True, 'manual', 32, '', True)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate*1e3)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)
        self.wes_costas_cc_0.set_natural_freq(self.nat_freq / (self.samp_rate*1000))

    def get_nat_freq(self):
        return self.nat_freq

    def set_nat_freq(self, nat_freq):
        self.nat_freq = nat_freq
        self.wes_costas_cc_0.set_natural_freq(self.nat_freq / (self.samp_rate*1000))

    def get_lw(self):
        return self.lw

    def set_lw(self, lw):
        self.lw = lw

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

    def get_bSignal(self):
        return self.bSignal

    def set_bSignal(self, bSignal):
        self.bSignal = bSignal
        self._bSignal_callback(self.bSignal)
        self.blocks_selector_0_0.set_input_index(self.bSignal)

    def get_bSelectPLL(self):
        return self.bSelectPLL

    def set_bSelectPLL(self, bSelectPLL):
        self.bSelectPLL = bSelectPLL
        self._bSelectPLL_callback(self.bSelectPLL)
        self.wes_costas_cc_0.set_loop_type(self.bSelectPLL)

    def get_axis(self):
        return self.axis

    def set_axis(self, axis):
        self.axis = axis



def main(top_block_cls=lab3, options=None):

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
