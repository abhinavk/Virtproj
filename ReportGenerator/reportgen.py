#!/usr/bin/python3

import fpdf
import argparse
import libvirt
import time
import subprocess


def get_filename(error=False):
    current_date = 'weekly-report-' + time.strftime('%Y-%m-%d')
    if error is True:
        return current_date + '-error.pdf'
    else:
        return current_date + '.pdf'

def print_host_info(p):
    host_info = conn.getInfo()
    p.set_font('Arial','B', 18)
    p.cell(0, 10, 'Host Info', 0, 1)
    
    # Set font for the Host Information table
    p.set_font('Arial', '', 14)
    
    p.cell(60, 10, 'Host name: ', 1, 0, 'R')
    p.cell(0, 10, conn.getHostname(), 1, 1)

    p.cell(60, 10, 'CPU Architecture: ', 1, 0, 'R')
    p.cell(0, 10, host_info[0], 1, 1)
    
    p.cell(60, 10, 'CPU Model: ', 1, 0, 'R')
    from_stdout = subprocess.check_output('cat /proc/cpuinfo | grep "model name"',shell=True)
    model = from_stdout.decode('utf-8').split('\n')[0].split(':')[1].strip()
    p.cell(0, 10, model, 1, 1)
    
    p.cell(60, 10, 'Memory Size: ', 1, 0, 'R')
    p.cell(0, 10, str(host_info[1]) + ' MB', 1, 1)
    
    p.cell(60, 10, 'Current CPU Clock: ', 1, 0, 'R')
    p.cell(0, 10, str(host_info[3]) + ' MHz', 1, 1)
    
    p.cell(60, 10, 'Number of CPU cores ', 1, 0, 'R')
    p.cell(0, 10, str(host_info[6]), 1, 1)
    
    p.cell(60, 10, 'Number of threads: ', 1, 0, 'R')
    p.cell(0, 10, str(host_info[6]*host_info[7]), 1, 1)
    
    p.cell(60, 10, 'Current hypervisor name: ', 1, 0, 'R')
    p.cell(0, 10, conn.getType(), 1, 1)
    
    p.cell(60, 10, 'Current hypervisor version', 1, 0, 'R')
    p.cell(0, 10, str(conn.getVersion()), 1, 1)
    
    p.cell(60, 10, 'Connection encrypted', 1, 0, 'R')
    p.cell(0, 10, 'Yes' if conn.isEncrypted() else 'No', 1, 1)

def gen_weekly_report():
    pdf = fpdf.FPDF()

    # Title Page
    pdf.add_page()

    # Print heading
    pdf.set_font('Arial','B',40)
    pdf.cell(0, 30, 'Generated Weekly report', 0, 1, 'C')

    print_host_info(pdf)

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

    gen_weekly_report()
