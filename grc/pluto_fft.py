#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Pluto FFT
# Description: Pluto FFT Waveform Plotter
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
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio.qtgui import Range, RangeWidget
import iio
import numpy
from gnuradio import qtgui

class pluto_fft(gr.top_block, Qt.QWidget):

    def __init__(self, fft_size=1024, freq=89.5, gain=32, samp_rate=1000, update_rate=.03):
        gr.top_block.__init__(self, "Pluto FFT")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Pluto FFT")
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

        self.settings = Qt.QSettings("GNU Radio", "pluto_fft")

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
        self.fft_size = fft_size
        self.freq = freq
        self.gain = gain
        self.samp_rate = samp_rate
        self.update_rate = update_rate

        ##################################################
        # Variables
        ##################################################
        self.samp_rate_ = samp_rate_ = samp_rate
        self.gain_ = gain_ = gain
        self.freq_c = freq_c = freq

        ##################################################
        # Blocks
        ##################################################
        self._samp_rate__tool_bar = Qt.QToolBar(self)
        self._samp_rate__tool_bar.addWidget(Qt.QLabel('Passband Bandwidth (kHz)' + ": "))
        self._samp_rate__line_edit = Qt.QLineEdit(str(self.samp_rate_))
        self._samp_rate__tool_bar.addWidget(self._samp_rate__line_edit)
        self._samp_rate__line_edit.returnPressed.connect(
            lambda: self.set_samp_rate_(eng_notation.str_to_num(str(self._samp_rate__line_edit.text()))))
        self.top_grid_layout.addWidget(self._samp_rate__tool_bar, 3, 2, 1, 2)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._gain__range = Range(0, 100, 1, gain, 200)
        self._gain__win = RangeWidget(self._gain__range, self.set_gain_, 'RX Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._gain__win, 2, 0, 1, 4)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freq_c_tool_bar = Qt.QToolBar(self)
        self._freq_c_tool_bar.addWidget(Qt.QLabel('Carrier Frequency (MHz)' + ": "))
        self._freq_c_line_edit = Qt.QLineEdit(str(self.freq_c))
        self._freq_c_tool_bar.addWidget(self._freq_c_line_edit)
        self._freq_c_line_edit.returnPressed.connect(
            lambda: self.set_freq_c(eng_notation.str_to_num(str(self._freq_c_line_edit.text()))))
        self.top_grid_layout.addWidget(self._freq_c_tool_bar, 3, 0, 1, 2)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.display = Qt.QTabWidget()
        self.display_widget_0 = Qt.QWidget()
        self.display_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.display_widget_0)
        self.display_grid_layout_0 = Qt.QGridLayout()
        self.display_layout_0.addLayout(self.display_grid_layout_0)
        self.display.addTab(self.display_widget_0, 'Spectrum')
        self.display_widget_1 = Qt.QWidget()
        self.display_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.display_widget_1)
        self.display_grid_layout_1 = Qt.QGridLayout()
        self.display_layout_1.addLayout(self.display_grid_layout_1)
        self.display.addTab(self.display_widget_1, 'Waterfall')
        self.display_widget_2 = Qt.QWidget()
        self.display_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.display_widget_2)
        self.display_grid_layout_2 = Qt.QGridLayout()
        self.display_layout_2.addLayout(self.display_grid_layout_2)
        self.display.addTab(self.display_widget_2, 'Scope')
        self.top_grid_layout.addWidget(self.display, 0, 0, 1, 4)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            samp_rate_*1000, #bw
            '', #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(update_rate)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.display_grid_layout_1.addWidget(self._qtgui_waterfall_sink_x_0_win, 0, 0, 1, 4)
        for r in range(0, 1):
            self.display_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 4):
            self.display_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate_*1000, #samp_rate
            '', #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(update_rate)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)

        self.qtgui_time_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
            '', '', '', '', '']
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
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.display_grid_layout_2.addWidget(self._qtgui_time_sink_x_0_win, 0, 0, 1, 4)
        for r in range(0, 1):
            self.display_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 4):
            self.display_grid_layout_2.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            fft_size, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            samp_rate_*1000, #bw
            '', #name
            1
        )
        self.qtgui_freq_sink_x_0.set_update_time(update_rate)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(True)

        self.qtgui_freq_sink_x_0.disable_legend()


        labels = ['', '', '', '', '',
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
        self.display_grid_layout_0.addWidget(self._qtgui_freq_sink_x_0_win, 0, 0, 1, 4)
        for r in range(0, 1):
            self.display_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 4):
            self.display_grid_layout_0.setColumnStretch(c, 1)
        self.iio_pluto_source_0 = iio.pluto_source('', int(freq_c*1e6), int(samp_rate_*1000), 20000000, 32768, True, True, True, 'manual', gain_, '', True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.iio_pluto_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "pluto_fft")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        self.fft_size = fft_size

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_freq_c(self.freq)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq, self.samp_rate_*1000)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.freq, self.samp_rate_*1000)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.set_gain_(self.gain)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samp_rate_(self.samp_rate)

    def get_update_rate(self):
        return self.update_rate

    def set_update_rate(self, update_rate):
        self.update_rate = update_rate
        self.qtgui_freq_sink_x_0.set_update_time(self.update_rate)
        self.qtgui_time_sink_x_0.set_update_time(self.update_rate)
        self.qtgui_waterfall_sink_x_0.set_update_time(self.update_rate)

    def get_samp_rate_(self):
        return self.samp_rate_

    def set_samp_rate_(self, samp_rate_):
        self.samp_rate_ = samp_rate_
        Qt.QMetaObject.invokeMethod(self._samp_rate__line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.samp_rate_)))
        self.iio_pluto_source_0.set_params(int(self.freq_c*1e6), int(self.samp_rate_*1000), 20000000, True, True, True, 'manual', self.gain_, '', True)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq, self.samp_rate_*1000)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate_*1000)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.freq, self.samp_rate_*1000)

    def get_gain_(self):
        return self.gain_

    def set_gain_(self, gain_):
        self.gain_ = gain_
        self.iio_pluto_source_0.set_params(int(self.freq_c*1e6), int(self.samp_rate_*1000), 20000000, True, True, True, 'manual', self.gain_, '', True)

    def get_freq_c(self):
        return self.freq_c

    def set_freq_c(self, freq_c):
        self.freq_c = freq_c
        Qt.QMetaObject.invokeMethod(self._freq_c_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.freq_c)))
        self.iio_pluto_source_0.set_params(int(self.freq_c*1e6), int(self.samp_rate_*1000), 20000000, True, True, True, 'manual', self.gain_, '', True)


def argument_parser():
    description = 'Pluto FFT Waveform Plotter'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--fft-size", dest="fft_size", type=intx, default=1024,
        help="Set Set number of FFT bins [default=%(default)r]")
    parser.add_argument(
        "-f", "--freq", dest="freq", type=eng_float, default="89.5",
        help="Set Default Frequency (MHz) [default=%(default)r]")
    parser.add_argument(
        "-g", "--gain", dest="gain", type=eng_float, default="32.0",
        help="Set Set gain in dB (default is midpoint) [default=%(default)r]")
    parser.add_argument(
        "-s", "--samp-rate", dest="samp_rate", type=eng_float, default="1.0k",
        help="Set Sample Rate [default=%(default)r]")
    parser.add_argument(
        "--update-rate", dest="update_rate", type=eng_float, default="30.0m",
        help="Set Set GUI widget update rate [default=%(default)r]")
    return parser


def main(top_block_cls=pluto_fft, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(fft_size=options.fft_size, freq=options.freq, gain=options.gain, samp_rate=options.samp_rate, update_rate=options.update_rate)
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
