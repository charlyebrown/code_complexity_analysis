import subprocess
import csv
import re
import sys


def run_mccabe(pyfile):
	cmd = "python -m mccabe %s" % pyfile
	return subprocess.check_output(cmd.split()).decode('utf-8')


def run_analysis(pyfile,output):
	mccabe_out = run_mccabe(pyfile).splitlines()
	parsed_lines = [parse_line(line) for line in mccabe_out]
	parsed_lines = filter(None,parsed_lines)
	with open(output,'w') as File: 
		csv.writer(File).writerows(parsed_lines)

def main(args):
	run_analysis(args.pyfile,args.output)

def parse_line(line):
	match = re.match("^(\d+)[^']+'([^']+)' (\d+)",line)
	if match:
		return match.groups()


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('pyfile', help='File to analyse')
	parser.add_argument("--output", default="test.csv")
	args = parser.parse_args()
	main(args)