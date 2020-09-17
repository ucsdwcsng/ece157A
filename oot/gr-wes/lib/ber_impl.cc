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
#include "ber_impl.h"

namespace gr {
  namespace wes {

    ber::sptr
    ber::make(int bits_per_byte, int reset_ber)
    {
      return gnuradio::get_initial_sptr
        (new ber_impl(bits_per_byte, reset_ber));
    }


    /*
     * The private constructor
     */
    ber_impl::ber_impl(int bits_per_byte, int reset_ber)
      : gr::block("ber",
              gr::io_signature::make(2, 2, sizeof(char)),
              gr::io_signature::make(1, 2, sizeof(float))),
              d_bits_per_byte(bits_per_byte),
              d_reset_ber(reset_ber)
    {
        d_errors = 0;
        d_bits = 0;
    }

    /*
     * Our virtual destructor.
     */
    ber_impl::~ber_impl()
    {
    }

    /*
    void
    ber_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      // <+forecast+> e.g. ninput_items_required[0] = noutput_items
    }
    // I decided not to use forecast this for this block
    */

    int
    ber_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const char *in1 = (const char *) input_items[0];
      const char *in2 = (const char *) input_items[1];
      float *out1 = (float *) output_items[0];
      float *out2 = (float *) output_items[1];

      // Do <+signal processing+>
      for( int i=0; i<noutput_items; i++){

          if( d_reset_ber == 0 ){
              d_errors = d_errors + calc_bit_errors(in1[i],in2[i],d_bits_per_byte);
              d_bits = d_bits + d_bits_per_byte;
          }

          if( d_bits > 0 ){
              out1[i] = (d_errors * 1.0) / (d_bits * 1.0);
              out2[i] = d_errors * 1.0;
          }
          else{
            out1[i] = 0.0;
            out2[i] = 0.0;
          }


      }

      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each (noutput_items);

      // Tell runtime system how many output items we produced.
      return noutput_items;
    } // general_wor

    void ber_impl::reset_stats(int reset_ber){

        d_reset_ber = reset_ber;

        // if reset_ber is true, reset the bit_errors and bits count
        d_errors = 0;
        d_bits = 0;

    } // void ber_impl::reset_stats(bool reset_ber){

    int ber_impl::calc_bit_errors(char in1, char in2, int bits_per_byte){

        int sum = 0;
        char out = in1 ^ in2;

        for( int i=0; i<bits_per_byte; i++){
            sum = sum + ( 1 & out>>i );
        }

        return sum;
    }

  } /* namespace wes */
} /* namespace gr */
