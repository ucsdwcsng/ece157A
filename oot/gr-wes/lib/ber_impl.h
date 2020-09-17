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

#ifndef INCLUDED_WES_BER_IMPL_H
#define INCLUDED_WES_BER_IMPL_H

#include <wes/ber.h>

namespace gr {
  namespace wes {

    class ber_impl : public ber
    {
     private:
      // Nothing to declare in this block.
      int d_errors;
      int d_bits;
      int d_bits_per_byte;
      int d_reset_ber;

     public:
      ber_impl(int bits_per_byte, int reset_ber);
      ~ber_impl();

      // Where all the action really happens
      //void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

      void reset_stats(int reset_ber);
      int calc_bit_errors(char in1, char in2, int bits_per_byte);
    };

  } // namespace wes
} // namespace gr

#endif /* INCLUDED_WES_BER_IMPL_H */
