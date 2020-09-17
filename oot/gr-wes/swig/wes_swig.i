/* -*- c++ -*- */

#define WES_API

%include "gnuradio.i"           // the common stuff

//load generated python docstrings
%include "wes_swig_doc.i"

%{
#include "wes/costas_cc.h"
#include "wes/ber.h"
%}

%include "wes/costas_cc.h"
GR_SWIG_BLOCK_MAGIC2(wes, costas_cc);
%include "wes/ber.h"
GR_SWIG_BLOCK_MAGIC2(wes, ber);
