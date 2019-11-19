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

def main(fname):
    """ Input file name; output a rearanged pdf file in the same folder
    The documentation uses a file with 44 pages as an example"""

    orig = Reader(open(fname, 'rb'))
    origpages = orig.pages
    new = Writer()

    nop = len(origpages)
    nop_booklet = int(math.ceil(nop / 4.0)) # = 11

    base = np.arange(nop_booklet) + 1
    base = 2 * base
    base = base[::-1]
    pages = []
    for i in base:
        num = nop_booklet * 4 + 1 # = 45
        pages.append(i)
        pages.append(num - i)
        pages.append(num - i + 1)
        pages.append(num - (num - i + 1))

    for i in pages:
        if i > nop:
            new.addBlankPage()
        else:
            idx = int(i - 1)
            new.addPage(origpages[idx])

    # save the modified pdf file
    fn = os.path.join(os.path.dirname(fname),
                      os.path.basename(fname) + ".booklet.pdf")
    with open(fn, 'wb') as f:
        new.write(f)
    print("File saved as {}".format(fn))


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage:")
        print("python booklet.py path/to/PDF/file \n")
        print("Setups for your printer:")
        print("\t1. Paper size: Tabloid (11*17 in) for academic papers, books, etc;")
        print("\t2. Layout: 2 pages per sheet. Set layout direction to normal 'Z' layout. Set two-sided to Short-Edge binding.")
        print("\t3. Scale to fit the page. An example setup for ARA&A:")
        print("\t\t162% on 11*17 Borderless")
    else:
        main(sys.argv[1])
