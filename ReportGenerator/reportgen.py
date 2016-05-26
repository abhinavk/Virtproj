#!/usr/bin/python3

import fpdf
import argparse
import libvirt


def gen_weekly():
    pdf = fpdf.FPDF()

    # Title Page
    pdf.add_page()

    # Print heading
    pdf.set_font('Arial','B',40)
    pdf.cell(40, 10, 'Generated Weekly report', 0, 1, 'C')

    print_host_info()

    # Write the PDF file
    pdf.output('weekly-report-2016-05-26.pdf','F')

if __name__ == '__main__':
    gen_weekly()
