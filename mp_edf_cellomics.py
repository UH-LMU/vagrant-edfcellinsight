#!/usr/bin/python
import glob
import logging
import math, sys, time
import multiprocessing
from optparse import OptionParser
import os
import re
import subprocess

IMAGEJ = "/home/vagrant/Fiji.app/ImageJ-linux64"
EDF = "/vagrant/edf_cellomics_process_headless.py"

# Create log file
logging.basicConfig(filename='/vagrant/edf.log', format='%(levelname)s:%(message)s', level=logging.DEBUG)

compute_output = "NOT_SET"

def edf(etc):
    print "etc " + etc.inputdir
    print "etc " + etc.field
    print "etc " + str(etc.stacks)
    print "etc " + etc.outputdir

    for s in stacks:
        channelfilterstr = "|".join(s)
        print channelfilterstr
        channelfilter = re.compile(channelfilterstr)
        fieldfiles = glob.glob(etc.inputdir + "/" + etc.field + "*")
        edfinput = []
        for f in fieldfiles:
            #print f
            if re.search(channelfilter, f):
                #print "match"
                edfinput.append(f)
        print "edfinput " + str(edfinput)
        edffile = etc.outputdir + "/" + etc.field + "_edf_" + '_'.join(s) + ".tif"
        if len(edfinput) > 0:
            print "edffile " + edffile
    
            cmd = [IMAGEJ,EDF,"-o '"+edffile+"'","'"+"' '".join(edfinput)+"'"]
            print " ".join(cmd)
            logging.info(" ".join(cmd))
            os.system(" ".join(cmd))
            print


parser = OptionParser()
parser.add_option('-s','--stacks', help='d0,d1:d2,d3,d4')
options,args = parser.parse_args()

dir_input = args[0]
dir_output_root = args[1]
print "dir_input " + dir_input
print "dir_output_root " + dir_output_root
stacks = []
for s in options.stacks.split(":"):
    stacks.append(s.split(","))
print "stacks" + str(stacks)

head,tail = os.path.split(dir_input)
print "tail " + tail
dir_output = os.path.join(dir_output_root,tail) + "_edf"
print "dir_output " + dir_output

# start timer
start_time = time.time()


# check if output directory has data already
if os.path.isdir(dir_output):
    olds = glob.glob(dir_output + "/*_edf.tif")
    if len(olds) > 0:
        print "Output directory and converted files exists, aborting."
        sys.exit(1)
else:
    print "Creating output directory " + dir_output
    os.makedirs(dir_output)

class EdfTaskConfig:
    def __init__(self,inputdir,field,stacks,outputdir):
        self.inputdir = inputdir
        self.field = field
        self.stacks = stacks
        self.outputdir = outputdir

# Convert the data
start_time_convert = time.time()
msg = "Converting..."
print msg 
logging.info(msg)
pool = multiprocessing.Pool(None)

reC01 = re.compile('(LMU-CELLINSIGHT_[0-9]{12}_[A-Z][0-9]{2}f[0-9]{2,3})')
files = glob.glob(dir_input + "/*.tiff")
fields = set()
for f in files:
    print "file" + f
    result = reC01.search(f)
    if result:
        fields.add(result.group(0))

tasks = []
for f in fields:
    print "field" + f
    task = EdfTaskConfig(dir_input,f,stacks,dir_output)
    tasks.append(task)

#r = pool.map(edf, tasks)
for t in tasks:
    edf(t)

logging.info("Time elapsed: " + str(time.time() - start_time_convert) + "s")


logging.info("Total time elapsed: " + str(time.time() - start_time) + "s")
print "Done."
