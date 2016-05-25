#!/usr/bin/python3

import fpdf
import argparse

def gen_weekly():
    pdf = fpdf.FPDF()

    # Title Page
    pdf.add_page()

    # Print heading
    pdf.set_font('Arial','B',20)
    pdf.cell(40,10,'Generated Weekly report')

    # Write the PDF file
    pdf.output('weekly-report-2016-05-26.pdf','F')

if __name__ == '__main__':
    gen_weekly()
