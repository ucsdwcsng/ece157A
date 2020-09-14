/* -*- c++ -*- */
/*
 * Copyright 2020 wes.
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

#ifndef INCLUDED_WES_SQUARE_FF_IMPL_H
#define INCLUDED_WES_SQUARE_FF_IMPL_H

#include <wes/square_ff.h>

//static sptr make(float fn, float zeta, int loop_type);

/*
costas_loop_cc::sptr costas_loop_cc::make(float loop_bw, int order, bool use_snr)
{
    return gnuradio::get_initial_sptr(new costas_loop_cc_impl(loop_bw, order, use_snr));
}

static int ios[] = { sizeof(gr_complex), sizeof(float), sizeof(float), sizeof(float) };
static std::vector<int> iosig(ios, ios + sizeof(ios) / sizeof(int));
*/

namespace gr {
  namespace wes {

    class square_ff_impl : public square_ff
    {
     private:
      // Nothing to declare in this block.

     public:
      square_ff_impl();
      ~square_ff_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

    };

  } // namespace wes
} // namespace gr

#endif /* INCLUDED_WES_SQUARE_FF_IMPL_H */

