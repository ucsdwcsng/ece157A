/* -*- c++ -*- */
/*
 * Copyright 2020 pling.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <gnuradio/expj.h>
#include <gnuradio/math.h>
#include <gnuradio/sincos.h>
#include "costas_cc_impl.h"

namespace gr {
  namespace wes {

    costas_cc::sptr
    costas_cc::make(float fn, float zeta, int loop_type)
    {
      return gnuradio::get_initial_sptr
        (new costas_cc_impl(fn, zeta, loop_type));
    }


    /*
     * The private constructor
     */
    costas_cc_impl::costas_cc_impl(float fn, float zeta, int loop_type)
      : gr::sync_block("costas_cc",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 2, sizeof(gr_complex))),
              d_natural_freq(fn),
              d_zeta(zeta),
              d_loop_type(loop_type)
    {
        set_natural_freq(fn);
        set_damping(zeta);
        set_loop_type(loop_type);
    }

    /*
     * Our virtual destructor.
     */
    costas_cc_impl::~costas_cc_impl()
    {
    }

    int
    costas_cc_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *) input_items[0];
      gr_complex *out = (gr_complex *) output_items[0];
      gr_complex *lfilt_out = (gr_complex *) output_items[1];

      // define the nco output
      gr_complex nco_out;
      gr_complex sample;

      std::vector<tag_t> tags;
      get_tags_in_range(tags,
                        0,
                        nitems_read(0),
                        nitems_read(0) + noutput_items,
                        pmt::intern("phase_est"));

      // inits
      float vco_out = 0;
      float vco_out_last = 0;
      float vco_in = 0;
      float vco_in_last = 0;
      float xI = 0;
      float xQ = 0;

      float e = 0;

      float f_in_last = 0;
      float f_out_last = 0;

      float f_in = 0;
      float f_out = 0;
      float f_int_out = 0;
      float f_int_out_last = 0;

      float Kt = 4.0*(3.141592653)*d_zeta*d_natural_freq;
      float a = (3.141592653)*d_natural_freq/d_zeta;

      for (int i = 0; i < noutput_items; i++) {
          if (!tags.empty()) {
              if (tags[0].offset - nitems_read(0) == (size_t)i) {
                  //d_phase = (float)pmt::to_double(tags[0].value);
                  tags.erase(tags.begin());
              }
          }

          // create nco out
          nco_out = gr_expj(-vco_out);

          // rotate the input by the adjusted phase est
          out[i] = in[i] * nco_out;

          // extract the sample
          sample = out[i];

          // create xI and xQ
          xI = sample.real();
          xQ = sample.imag();

          // e is the phase error
          if( d_loop_type == 0)
          {
              // standard loop
              e = xQ;
          }
          else if( d_loop_type == 1)
          {
              // costas loop
              e = xI*xQ;
          }
          else if( d_loop_type == 2)
          {
              // costas w/ hardlimiter
              if( xI >= 0)
                xI = 1;
              else
                xI = -1;

              e = xI * xQ;
          }
          else if( d_loop_type == 3)
          {
              // qpsk "costas"
              e = xI*xQ*( xI*xI - xQ*xQ);
          }
          else
          {
              // by default, choose the standard loop
              e = xQ;
          }

          // apply phase error gain Kt
          // f_in is t he loop filter in
          f_in = Kt*e;

          // integral part
          f_int_out = f_int_out_last + a*(0.5)*(f_in + f_in_last);

          // proportional part + integral part
          f_out = f_in +  f_int_out;

          // update_gains
          f_in_last = f_in;
          vco_in = f_out;
          f_out_last = f_out;
          f_int_out_last = f_int_out;

          // update loop filter output
          lfilt_out[i] = f_out;

          // update vco
          vco_out = vco_out_last + (0.5)*(vco_in + vco_in_last);
          vco_out_last = vco_out;
          vco_in_last = vco_in;

      } // for (int i = 0; i < noutput_items; i++) {

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }// work

    void costas_cc_impl::set_natural_freq(float fn){
        d_natural_freq = fn;
    }

    void costas_cc_impl::set_damping(float zeta){
        d_zeta = zeta;
    }

    void costas_cc_impl::set_loop_type(int loop_type){
        d_loop_type = loop_type;
    }

  } /* namespace wes */
} /* namespace gr */
