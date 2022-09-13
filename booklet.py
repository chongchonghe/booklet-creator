#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A script to rearrange the order of a PDF document so that if
printed in Tabloid style, it reads like a book.

Here is how it works: 
E.g., for a document with 8 pages, this code rearranges the pages to
the following order:
4, 5, 6, 3, 2, 7, 8, 1

@author: ChongChong He, on Nov 19, 2019. Tested with Python 3.6.7 on
macOS. Contact: chongchong@astro.umd.edu

"""

import sys
import os
import math
import numpy as np
from PyPDF2 import PdfFileWriter as Writer, PdfFileReader as Reader
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="""
A python program to rearrange the order of a PDF document so that if printed in Tabloid style, it reads like a book.\n
The setting of your printer should be:
\t(1). Paper size: Tabloid (11*17 in) for academic papers, books, etc;
\t(2). Layout: 2 pages per sheet. Set layout direction to normal 'Z' layout. Set two-sided to Short-Edge binding.
\t(3). Scale to fit the page. An example setup for ARA&A:
\t\t162% on 11*17 Borderless""")
    parser.add_argument(dest='pdffile', type=str, help="The PDF file to convert")
    parser.add_argument('-s', '--start', default=1, type=int, help="The starting page number")
    parser.add_argument('-e', '--end', type=int, help="The ending page number")
    parser.add_argument('-p', '--print-pages', action="store_true",
                        help="Toggle printing the page numbers (and won't rearange the PDF)")
    return parser.parse_args()

def main(fname, start=1, end=None, print_page=False):
    """ Input file name; output a rearanged pdf file in the same folder
    An imaginary documentation has 41 pages in the comments """

    orig = Reader(open(fname, 'rb'))
    origpages = orig.pages
    nop = len(origpages)
    assert nop >= 4, "Number of pages must not be less than 4"
    if end is not None:
        assert start is not None
        assert end <= nop
        nop = end - start + 1

    new = Writer()
    nop_booklet = nop // 4
    if nop % 4 > 0:
        nop_booklet += 1 # = 11

    base = np.arange(nop_booklet) + 1  # = 1, 2, ... 11
    base = 2 * base                    # = 2, 4, ... 22
    base = base[::-1]                  # = 22, 21, ... 2
    pages = []
    num = nop_booklet * 4 + 1 # = 45
    for i in base:
        pages.append(i)
        pages.append(num - i)
        pages.append(num - i + 1)
        pages.append(num - (num - i + 1))

    if print_page:
        print("The pages will be reordered as", pages)
        return

    for i in pages:
        if i > nop:
            new.addBlankPage()
        else:
            idx = int(i + start - 1 - 1)
            new.addPage(origpages[idx])

    # save the modified pdf file
    fn = os.path.join(os.path.dirname(fname),
                      os.path.basename(fname) + ".booklet.pdf")
    print(fn)
    # return
    with open(fn, 'wb') as f:
        new.write(f)
    print("File saved as {}".format(fn))


if __name__ == "__main__":

    args = parse_arguments()
    main(args.pdffile, args.start, args.end, args.print_pages)
