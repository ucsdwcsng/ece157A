#!/usr/bin/env bash

# copy .hier file cache
echo "Installing Hier Files..."

mkdir ~/.grc_gnuradio
cp -r hier_cache/* ~/.grc_gnuradio
cd oot/gr-wes

rm -rf build
mkdir build
cd build
cmake ..
make
sudo make install

echo "Code Compilation Complete... "

sudo ldconfig

echo "Blocks Updated..."
