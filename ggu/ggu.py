#! /usr/bin/env python
# Grab, Gimp, Upload

import os, sys, subprocess, time, errno, getpass
from ftplib import FTP
from optparse import OptionParser

# Parse Command Line
parser = OptionParser()
parser.add_option("-r", "--rotate", type="string", dest="rotate", default="90>")
parser.add_option("--resize", type="string", dest="resize", default="500")
parser.add_option("--user", type="string", dest="ftp_user", default="cantlin")
parser.add_option("--host", type="string", dest="ftp_host", default="greysbooks.co.uk")
parser.add_option("--password", type="string", dest="ftp_password", default=False)
parser.add_option("--remote-dir", type="string", dest="ftp_remote_dir", default="/httpdocs/upload")
parser.add_option("-c", "--no-capture", action="store_true", dest="no_capture", default=False)
parser.add_option("-p", "--no-process", action="store_true", dest="no_process", default=False)
parser.add_option("-u", "--no-upload", action="store_true", dest="no_upload", default=False)
parser.add_option("--local-dir", type="string", dest="local_dir", default=False)
parser.add_option("--base-cmd", type="string", dest="base_cmd", default="mogrify")
parser.add_option("--glob", type="string", dest="glob", default="*.JPG")

(options, args) = parser.parse_args()   

print "Starting..."

def mkdir_p(path):
    """Functions like mkdir -p."""
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise
        
# Working directory   
if not options.local_dir:
    today = time.strftime("%d-%m-%Y")
    new_dir = os.getcwd() + "/" + today
else:
    new_dir = options.local_dir
    

print "Using directory \"" + new_dir + "\"..."

mkdir_p(new_dir)
os.chdir(new_dir)

if options.no_capture:
    print "Skipping gphoto2..."
else:
    # Copy all images from camera to pwd
    print "\nInitiating gphoto2..."
    cmd=["gphoto2", "--get-all-files"]
    assert subprocess.call(cmd)==0, 'Error in cmd: %s' % cmd # Returncode should be zero
    
if options.no_process:
    print "Skipping image processing..."
else:
    print "\nDoing ImageMagick...\n"
    print "Rotating..."
    cmd = [options.base_cmd, "-rotate", options.rotate, options.glob]
    assert subprocess.call(cmd)==0, "Error in: %s" %cmd
    print "Cropping left..."
    cmd = [options.base_cmd, "-crop", "+100+0", "+repage", options.glob]
    assert subprocess.call(cmd)==0, "Error in: %s" %cmd
    print "Cropping right..."
    cmd = [options.base_cmd, "-crop", "-100+0", "+repage", options.glob]
    assert subprocess.call(cmd)==0, "Error in: %s" %cmd
    print "Resizing..."
    cmd = [options.base_cmd, "-resize", options.resize, options.glob]
    assert subprocess.call(cmd)==0, "Error in: %s" %cmd
    print "Normalizing...\n"
    cmd = [options.base_cmd, "-normalize", options.glob]
    assert subprocess.call(cmd)==0, "Error in: %s" %cmd
    
if options.no_upload:
    print "Skipping upload..."
else:
    if not options.ftp_password:
        options.ftp_password = getpass.getpass("Password for \"" + options.ftp_user + "@" + options.ftp_host + "\":")
        
    # Upload images
    print "Connecting to \"" + options.ftp_host + "\"...\n"

    ftp = FTP(options.ftp_host)
    ftp.login(options.ftp_user, options.ftp_password)

    print ftp.getwelcome()
    ftp.cwd(options.ftp_remote_dir)

    print "Using remote directory \" " + options.ftp_remote_dir + "\"..."

    for root, dirs, files in os.walk(new_dir):
        for fname in files:
            print "Storing " + fname + "..."
            full_fname = os.path.join(root, fname)
            ftp.storbinary('STOR ' + fname, open(full_fname, 'rb'))
        
    

print "Done."
