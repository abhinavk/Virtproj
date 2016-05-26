+#!/usr/bin/python3

import fpdf
import argparse
import libvirt
import time


def get_filename(error=False):
    current_date = 'weekly-report' + time.strftime('%Y-%m-%d')
    if error is True:
        return current_date + '-error.pdf'
    else:
        return current_date + '.pdf'

def gen_weekly():
    pdf = fpdf.FPDF()

    # Title Page
    pdf.add_page()

    # Print heading
    pdf.set_font('Arial','B',40)
    pdf.cell(40, 10, 'Generated Weekly report', 0, 1, 'C')

    print_host_info()

    # Write the PDF file
    pdf.output(get_filename(),'F')

def gen_error_pdf():
    errorpdf = fpdf.FPDF()
    errorpdf.add_page()
    errorpdf.set_font('Arial','B',48)
    errorpdf.cell(40, 40, 'Error connecting to Qemu. Terminating report generation.', 0, 0, 'C')
    pdf.output(get_filename(error=True),'F')

if __name__ == '__main__':
    # Make connection to libvirt
    conn = libvirt.open("qemu:///system")

    if conn is None:
        print("No Qemu instance running.", file=sys.stderr)
        gen_error_pdf()
        exit(1)

    gen_weekly()
