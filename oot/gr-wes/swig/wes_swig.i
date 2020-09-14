/* -*- c++ -*- */

#define WES_API

%include "gnuradio.i"           // the common stuff

//load generated python docstrings
%include "wes_swig_doc.i"

%{
#include "wes/square_ff.h"
#include "wes/wes_costas_cc.h"
%}

%include "wes/square_ff.h"
GR_SWIG_BLOCK_MAGIC2(wes, square_ff);
%include "wes/wes_costas_cc.h"
GR_SWIG_BLOCK_MAGIC2(wes, wes_costas_cc);
