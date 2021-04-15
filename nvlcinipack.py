#!/usr/bin/python

# Copyright (C) 2021 Mellanox Technologies, Ltd. ALL RIGHTS RESERVED.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import struct
import os

def get_args():
    parser = argparse.ArgumentParser(prog="nvlcinipack",
                                     description="Pack multiple line card ini files into one file in format [le16 size_1, ini_1][le16 size_2, ini_2]..[le16 size_n, ini_n]")
    parser.add_argument("-i", "--input", action='append', help="input ini file. Multiple files could be passed.", required=True)
    parser.add_argument("-o", "--output", help="output pack file. In case the name ends with \".xz\", LZMA compression is going to be used.", required=True)
    return parser.parse_args()

args = get_args()

magic = "NVLCINI+".encode('ascii')

if args.output.endswith(".xz"):
    import lzma

    fo = lzma.open(args.output, mode='wb', format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC32)
    print("output is XZ archive")
else:
    fo = open(args.output, mode='wb')
    print("output is plain data file")

fo.write(magic)

for ifile in args.input:
    size = os.stat(ifile).st_size
    print("packing file %s of size %d bytes" % (ifile, size))

    fo.write(struct.pack("<H", size))
    with open(ifile, mode='rb') as fi:
        fo.write(fi.read())
