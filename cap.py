#! /usr/bin/env python
# Take a screenshot and upload it somewhere.

import os, sys, subprocess, time, errno, getpass
from ftplib import FTP
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-d", "--dir", type="string", dest="local_dir", default="/Users/Cantlin/screenshots")
parser.add_option("-f", "--file", type="string", dest="file_name", default=False)
parser.add_option("--format", type="string", dest="file_format", default="png")
parser.add_option("-r", "--remote-dir", type="string", dest="ftp_remote_dir", default="/httpdocs/pub")
parser.add_option("-u", "--user", type="string", dest="ftp_user", default="cantl.in")
parser.add_option("--host", type="string", dest="ftp_host", default="cantl.in")
parser.add_option("--uri", type="string", dest="base_uri", default="http://cantl.in/pub/")
parser.add_option("-p", "--password", type="string", dest="ftp_password", default=False)
(options, args) = parser.parse_args()   

os.chdir(options.local_dir)
file_name = options.file_name if options.file_name else "ss_" + str(int(time.time()))
file_name += '.' +  options.file_format
subprocess.call(['screencapture', '-m', '-T3', '-t' + options.file_format, file_name])
    
if not options.ftp_password:
    options.ftp_password = getpass.getpass("Password for \"" + options.ftp_user + "@" + options.ftp_host + "\": ")
    
ftp = FTP(options.ftp_host)
ftp.login(options.ftp_user, options.ftp_password)
print ftp.getwelcome()
ftp.cwd(options.ftp_remote_dir)
full_path = os.path.join(options.local_dir, file_name)
ftp.storbinary('STOR ' + file_name, open(full_path, 'rb'))

remote_path = options.base_uri + file_name
print "\nLocal:  " + full_path
print "Remote: " + remote_path
subprocess.call(['open', remote_path])
