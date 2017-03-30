import subprocess
import csv
import re
import sys


def run_mccabe(pyfile):
	cmd = "python -m mccabe %s" % pyfile
	return subprocess.check_output(cmd.split()).decode('utf-8')


def main(args):
	mccabe_out = run_mccabe(args.pyfile).splitlines()
	parsed_lines = [parse_line(line) for line in mccabe_out]
	with open(args.output,'w') as File: 
		csv.writer(File).writerows(parsed_lines)


def parse_line(line):
	return re.match("^(\d+)[^']+'([^']+)' (\d+)",line).groups()


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('pyfile', help='File to analyse')
	parser.add_argument("--output", default="test.csv")
	args = parser.parse_args()
	main(args)