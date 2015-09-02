#!/usr/bin/env python

import collections, os, uuid, logging, time, signal, sys
from random import randint

file_logging = True
log_file = "gendatafile.log"
file_logging_maxsize = 20480000										# max file size (bytes)
file_logging_keep_count = 10										# number of log files to keep
file_logging_level = logging.DEBUG 									# minimum log level to write to log file
console_logging = True
console_logging_level = logging.DEBUG

words = open("/Users/dstoll/scripts/lorem.txt", "r").read().replace("\n", '').split()
seed = "1092384956781341341234656953214543219"

def signal_handler(signal, frame):
	logger.warn("Caught signal.  Exiting")
	sys.exit(0)
	
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGQUIT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# logging setup
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)s - %(funcName)s() - %(levelname)s - %(message)s')

# file logging
if file_logging:
	from logging.handlers import RotatingFileHandler
	file_log_handler = RotatingFileHandler(log_file, maxBytes=file_logging_maxsize, backupCount=file_logging_keep_count)
	file_log_handler.setLevel(file_logging_level)
	file_log_handler.setFormatter(formatter)
	logger.addHandler(file_log_handler)

# console logging
if console_logging:
	console_handler = logging.StreamHandler()
	console_handler.setLevel(console_logging_level)
	console_handler.setFormatter(formatter)
	logger.addHandler(console_handler)

def fdata():
    a = collections.deque(words)
    b = collections.deque(seed)
    while True:
        yield ' '.join(list(a)[0:1024])
        a.rotate(int(b[0]))
        b.rotate(1)


def create_file(filename = None, size=None):
	"""
	Create a datafile.  
	If filename and size are specified, they will be obeyed. 
	Otherwise, a random filename will be created as a uuid4 and .txt appended.
	A random size between 1k and 5MB will be chosen.
	"""
	logger.debug("creating a datafile.")

	g = fdata()

	if size == None:
		size = randint(1024, 5120000)  # set size to random number between 1k and 5MB
		logger.debug("size not specified, setting size to: %d" %size)

	if filename == None:
		filename = uuid.uuid4().hex + ".txt"
		logger.debug("filename not specified, setting filename to: %s" %filename)

	fh = open(filename, 'w')
	while os.path.getsize(filename) < size:
	    fh.write(g.next())
	
	logger.info("created file: %s, size: %d" %(filename, os.path.getsize(filename)))

def main():
	logger.info("starting random data creation.")

	while(True):
		numfiles = randint(1,10)
		logger.info("creating %d data files." %numfiles)

		for i in range(1,numfiles):
			create_file()

		sleeptime = randint(60,600)
		logger.info("sleeping for %d seconds" %sleeptime)

		time.sleep(sleeptime)

if __name__ == "__main__":
	main()
