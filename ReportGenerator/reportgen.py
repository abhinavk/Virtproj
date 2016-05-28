#!/usr/bin/python3

import fpdf
import argparse
import libvirt
import sqlite3
import time
import datetime as dt
import subprocess
from xml.dom import minidom

COL_WIDTH = 70 # Width in millimetres for Column Width in tables
STD_HEIGHT = 10 # Standard height for cells

def get_filename(error=False):
    current_date = 'weekly-report-' + time.strftime('%Y-%m-%d')
    if error is True:
        return current_date + '-error.pdf'
    else:
        return current_date + '.pdf'

def none2z(string_from_db):
    if string_from_db is None:
        return str(0)
    else:
        return str(format(string_from_db, '.02f'))

def write_host_page(p,rd):
    p.add_page()
    p.set_font('Arial','B', 18)
    p.cell(0, STD_HEIGHT, 'Host Info', 0, 1)
    write_host_info(p)

    p.add_page()
    p.set_font('Arial','B', 18)
    p.cell(0, STD_HEIGHT, 'Host Resource Usage Report', 0, 1)
    write_host_usage(p,rd)

def write_host_usage(p,rd):
    # Set a smaller font for resource usage page
    p.set_font('Arial', 'B', 14)
    p.ln(5)

    # Headers of the table
    p.cell(40, STD_HEIGHT, 'Timeframe', 1, 0, 'C')
    p.cell(30, STD_HEIGHT, 'CPU', 1, 0, 'C')
    p.cell(30, STD_HEIGHT, 'Memory', 1, 0, 'C')
    p.cell(30, STD_HEIGHT, 'Temp', 1, 0, 'C')
    p.cell(30, STD_HEIGHT, 'Power', 1, 0, 'C')
    p.cell(30, STD_HEIGHT, 'Network', 1, 1, 'C')

    p.set_font('Arial', '', 14)

    # Weekly
    if isinstance(rd, list):
        startdate = dt.datetime.strptime(rd[0], "%Y-%m-%d")
        enddate = dt.datetime.strptime(rd[1], "%Y-%m-%d")
        delta = enddate - startdate

        for i in range(delta.days + 1):
            thisdate = startdate + dt.timedelta(days=i) # Iterate over all days
            p.cell(40, STD_HEIGHT, thisdate.strftime("%d-%m-%Y"), 1, 0, 'C')
            print(thisdate.strftime("%Y-%m-%d"))
            query = 'SELECT AVG(cpu),AVG(mem),AVG(temp),SUM(power),AVG(netRead + netWrite) FROM hostData WHERE dated is ?'
            c.execute(query, (thisdate.strftime("%Y-%m-%d"),))
            daydata = c.fetchone()

            p.cell(30, STD_HEIGHT, none2z(daydata[0]), 1, 0, 'C')
            p.cell(30, STD_HEIGHT, none2z(daydata[1]), 1, 0, 'C')
            p.cell(30, STD_HEIGHT, none2z(daydata[2]), 1, 0, 'C')
            p.cell(30, STD_HEIGHT, none2z(daydata[3]), 1, 0, 'C')
            p.cell(30, STD_HEIGHT, none2z(daydata[4]), 1, 1, 'C')
    # Daily
    else:
        for j in range(24): # for 24 hours of the day
            hour = format(j, '02d')
            p.cell(40, STD_HEIGHT, hour + ':00 - ' + hour + ':59', 1, 0, 'C')

            query = 'SELECT AVG(cpu),AVG(mem),AVG(temp),SUM(power),AVG(netRead + netWrite) FROM hostData WHERE dated is ? AND timed BETWEEN \"'
            c.execute(query + hour + ':00:00\" AND \"' + hour + ':59:59\"', (rd,))
            hourdata = c.fetchone()

            p.cell(30, STD_HEIGHT, none2z(hourdata[0]), 1, 0, 'C')
            p.cell(30, STD_HEIGHT, none2z(hourdata[1]), 1, 0, 'C')
            p.cell(30, STD_HEIGHT, none2z(hourdata[2]), 1, 0, 'C')
            p.cell(30, STD_HEIGHT, none2z(hourdata[3]), 1, 0, 'C')
            p.cell(30, STD_HEIGHT, none2z(hourdata[4]), 1, 1, 'C')


def write_host_info(p):
    # Set font for the Host Information table
    p.set_font('Arial', '', 14)

    p.cell(COL_WIDTH, STD_HEIGHT, 'Host name: ', 1, 0, 'R')
    p.cell(0, STD_HEIGHT, conn.getHostname(), 1, 1)

    p.cell(COL_WIDTH, STD_HEIGHT, 'CPU Architecture: ', 1, 0, 'R')
    p.cell(0, STD_HEIGHT, host_info[0], 1, 1)

    p.cell(COL_WIDTH, STD_HEIGHT, 'CPU Model: ', 1, 0, 'R')
    from_stdout = subprocess.check_output('cat /proc/cpuinfo | grep "model name"',shell=True)
    model = from_stdout.decode('utf-8').split('\n')[0].split(':')[1].strip()
    p.cell(0, STD_HEIGHT, model, 1, 1)

    p.cell(COL_WIDTH, STD_HEIGHT, 'Memory Size: ', 1, 0, 'R')
    p.cell(0, STD_HEIGHT, str(host_info[1]) + ' MB', 1, 1)

    p.cell(COL_WIDTH, STD_HEIGHT, 'Current CPU Clock: ', 1, 0, 'R')
    p.cell(0, STD_HEIGHT, str(host_info[3]) + ' MHz', 1, 1)

    p.cell(COL_WIDTH, STD_HEIGHT, 'Number of CPU cores ', 1, 0, 'R')
    p.cell(0, STD_HEIGHT, str(host_info[6]), 1, 1)

    p.cell(COL_WIDTH, STD_HEIGHT, 'Number of threads: ', 1, 0, 'R')
    p.cell(0, STD_HEIGHT, str(host_info[6]*host_info[7]), 1, 1)

    p.cell(COL_WIDTH, STD_HEIGHT, 'Current hypervisor name: ', 1, 0, 'R')
    p.cell(0, STD_HEIGHT, conn.getType(), 1, 1)

    p.cell(COL_WIDTH, STD_HEIGHT, 'Current hypervisor version: ', 1, 0, 'R')
    p.cell(0, STD_HEIGHT, str(conn.getVersion()), 1, 1)

    p.cell(COL_WIDTH, STD_HEIGHT, 'Connection encrypted', 1, 0, 'R')
    p.cell(0, STD_HEIGHT, 'Yes' if conn.isEncrypted() else 'No', 1, 1)

def write_domain_page(p,i,domain,rd):
    p.add_page()
    host_info = conn.getInfo()
    p.set_font('Arial','B', 18)
    p.cell(0, STD_HEIGHT, 'Domain Info for ' + domain.name() , 0, 1)
    write_domain_info(p,domain)

    p.add_page()
    p.set_font('Arial','B', 18)
    p.cell(0, STD_HEIGHT, 'Domain Resource Usage Report', 0, 1)
    write_domain_usage(p,i,rd)

def write_domain_usage(p,i,rd):
    # Set a smaller font for resource usage page
    p.set_font('Arial', 'B', 14)
    p.ln(5)

    # Headers of the table
    p.cell(50, STD_HEIGHT, 'Timeframe', 1, 0, 'C')
    p.cell(30, STD_HEIGHT, 'CPU', 1, 0, 'C')
    p.cell(30, STD_HEIGHT, 'Memory', 1, 0, 'C')
    p.cell(30, STD_HEIGHT, 'Network In', 1, 0, 'C')
    p.cell(30, STD_HEIGHT, 'Network Out', 1, 1, 'C')

    p.set_font('Arial', '', 14)

    vm = 'domDataVM' + str(i+1)

    # Weekly
    if isinstance(rd, list):
        startdate = dt.datetime.strptime(rd[0], "%Y-%m-%d")
        enddate = dt.datetime.strptime(rd[1], "%Y-%m-%d")
        delta = enddate - startdate

        for i in range(delta.days + 1):
            thisdate = startdate + dt.timedelta(days=i) # Iterate over all days
            p.cell(50, STD_HEIGHT, thisdate.strftime("%d-%m-%Y"), 1, 0, 'C')

            query = 'SELECT AVG(cpu),AVG(mem),AVG(netRead),AVG(netWrite) FROM ' + vm + ' WHERE dated is ?'
            c.execute(query, (thisdate.strftime("%Y-%m-%d"),))
            daydata = c.fetchone()

            p.cell(30, STD_HEIGHT, none2z(daydata[0]), 1, 0, 'C')
            p.cell(30, STD_HEIGHT, none2z(daydata[1]), 1, 0, 'C')
            p.cell(30, STD_HEIGHT, none2z(daydata[2]), 1, 0, 'C')
            p.cell(30, STD_HEIGHT, none2z(daydata[3]), 1, 1, 'C')
    # Daily
    else:
        for j in range(24): # for 24 hours of the day
            hour = format(j, '02d')
            p.cell(50, STD_HEIGHT, hour + ':00 - ' + hour + ':59', 1, 0, 'C')

            query = 'SELECT AVG(cpu),AVG(mem),AVG(netRead),AVG(netWrite) FROM ' + vm + ' WHERE dated is ? AND timed BETWEEN \"'
            c.execute(query + hour + ':00:00\" AND \"' + hour + ':59:59\"', (rd,))
            hourdata = c.fetchone()

            p.cell(30, STD_HEIGHT, none2z(hourdata[0]), 1, 0, 'C')
            p.cell(30, STD_HEIGHT, none2z(hourdata[1]), 1, 0, 'C')
            p.cell(30, STD_HEIGHT, none2z(hourdata[2]), 1, 0, 'C')
            p.cell(30, STD_HEIGHT, none2z(hourdata[3]), 1, 1, 'C')


def write_domain_info(p,domain):
    # Set font for the Host Information table
    p.set_font('Arial', '', 14)

    p.cell(COL_WIDTH, STD_HEIGHT, 'Domain ID: ', 1, 0, 'R')
    p.cell(0, STD_HEIGHT, str(domain.ID()), 1, 1)

    p.cell(COL_WIDTH, STD_HEIGHT, 'CPU cores allocated: ', 1, 0, 'R')
    p.cell(0, STD_HEIGHT, str(len(domain.vcpus()[0])), 1, 1)

    p.cell(COL_WIDTH, STD_HEIGHT, 'CPU core architecture: ', 1, 0, 'R')
    p.cell(0, STD_HEIGHT, 'x86', 1, 1)

    p.cell(COL_WIDTH, STD_HEIGHT, 'CPU Threads', 1, 0, 'R')
    p.cell(0, STD_HEIGHT, str(host_info[6]*host_info[7]), 1, 1)

    p.cell(COL_WIDTH, STD_HEIGHT, 'Operating System type: ', 1, 0, 'R')
    p.cell(0, STD_HEIGHT, domain.OSType(), 1, 1)

    p.cell(COL_WIDTH, STD_HEIGHT, 'Memory allocated: ', 1, 0, 'R')
    p.cell(0, STD_HEIGHT, str(domain.maxMemory()/1024), 1, 1)

    p.cell(COL_WIDTH, STD_HEIGHT, 'Memory currently in use: ', 1, 0, 'R')
    p.cell(0, STD_HEIGHT, str(domain.memoryStats()['rss']/1024) + ' MB', 1, 1)

    p.cell(COL_WIDTH, STD_HEIGHT, 'Disk file path: ', 1, 0, 'R')
    rxml = domain.XMLDesc(0)
    xml = minidom.parseString(rxml)
    disks = xml.getElementsByTagName("disk")
    sources = disks[0].childNodes
    for source in sources:
        if source.nodeName == "source":
            disk_file = str(source.attributes["file"].value)
    p.cell(0, STD_HEIGHT, disk_file, 1, 1)

    p.cell(COL_WIDTH, STD_HEIGHT, 'Current hypervisor name: ', 1, 0, 'R')
    p.cell(0, STD_HEIGHT, conn.getType(), 1, 1)

    p.cell(COL_WIDTH, STD_HEIGHT, 'Current hypervisor version: ', 1, 0, 'R')
    p.cell(0, STD_HEIGHT, str(conn.getVersion()), 1, 1)

    p.cell(COL_WIDTH, STD_HEIGHT, 'Autostarts on host boot: ', 1, 0, 'R')
    p.cell(0, STD_HEIGHT, 'Yes' if domain.autostart else 'No', 1, 1)


def gen_error_pdf():
    errorpdf = fpdf.FPDF()
    errorpdf.add_page()
    errorpdf.set_font('Arial','B',48)
    errorpdf.cell(40, 40, 'Error connecting to Qemu. Terminating report generation.', 0, 0, 'C')
    pdf.output(get_filename(error=True),'F')

def gen_weekly_report(dates):
    pdf = fpdf.FPDF()

    # Title Page
    pdf.add_page()

    # Print heading
    pdf.ln(50)
    pdf.set_font('Arial','B',40)
    pdf.cell(0, 30, 'Weekly report', 0, 1, 'C')
    pdf.set_font('Arial', '', 16)
    pdf.cell(0, 30, 'Generated at ' + time.strftime("%d-%m-%Y %H:%M:%S"), 0, 1, 'C')
    pdf.set_font('Arial', '', 20)
    pdf.cell(0, 30, 'Generated for ' + dates[0] + ' to ' + dates[1])

    write_host_page(pdf,dates)

    domains = conn.listAllDomains(0)
    for i,d in enumerate(domains):
        write_domain_page(pdf,i,d,dates)

    # Write the PDF file
    pdf.output(get_filename(),'F')

def gen_daily_report(rdate):
    pdf = fpdf.FPDF()

    # Title Page
    pdf.add_page()

    # Print heading
    pdf.ln(50)
    pdf.set_font('Arial','B',40)
    pdf.cell(0, 30, 'Daily report', 0, 1, 'C')
    pdf.set_font('Arial', '', 16)
    pdf.cell(0, 30, 'Generated at ' + time.strftime("%d-%m-%Y %H:%M:%S"), 0, 1, 'C')
    pdf.set_font('Arial', '', 20)
    pdf.cell(0, 30, 'Generated for ' + rdate, 0, 1, 'C')

    write_host_page(pdf,rdate)

    domains = conn.listAllDomains(0)
    for i,d in enumerate(domains):
        write_domain_page(pdf,i,d,rdate)

    # Write the PDF file
    pdf.output(get_filename(),'F')

if __name__ == '__main__':
    # Get today
    today = time.strftime('%Y-%m-%d')
    sevendaysago = (dt.date.today() - dt.timedelta(days=7)).strftime('%Y-%m-%d')

    parser = argparse.ArgumentParser(description='Generate reports')
    parser.add_argument('--daily', nargs='?')
    parser.add_argument('--weekly', nargs=2)
    argus = parser.parse_args()

    # Make connection to libvirt
    conn = libvirt.open("qemu:///system")
    host_info = conn.getInfo()

    if conn is None:
        print("No Qemu instance running.", file=sys.stderr)
        gen_error_pdf()
        exit(1)

    sqc = sqlite3.connect('../BackgroundSvc/RawData.db')
    c = sqc.cursor()

    if argus.weekly:
        gen_weekly_report(argus.weekly)
    if argus.daily:
        gen_daily_report(argus.daily)

    sqc.close()
