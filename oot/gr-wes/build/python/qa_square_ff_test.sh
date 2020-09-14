#!/usr/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir="/home/wes/gnuradio/gr-wes/python"
export GR_CONF_CONTROLPORT_ON=False
export PATH="/home/wes/gnuradio/gr-wes/build/python":$PATH
export LD_LIBRARY_PATH="":$LD_LIBRARY_PATH
export PYTHONPATH=/home/wes/gnuradio/gr-wes/build/swig:$PYTHONPATH
/usr/bin/python3 /home/wes/gnuradio/gr-wes/python/qa_square_ff.py 
