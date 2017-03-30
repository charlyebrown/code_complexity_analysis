import csv
from .analysis import run_analysis
import requests
import tempfile
# from from bokeh.charts import Bar, output_file, show
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool, Range1d, LabelSet, Label

def main(args):
	run_analysis(get_file(args.pyfile	),"test.csv")
	with open("test.csv") as f:
		file_data = list(csv.reader(f))
	plot(file_data,args.output)

def get_file(file_or_arg_url):
	if file_or_arg_url.startswith('http'):
		response = requests.get(file_or_arg_url)
		response.raise_for_status()
		temp = tempfile.mktemp()
		with open(temp,"w") as f:
			f.write(response.text)
		return temp
	return file_or_arg_url

def plot(data,file_output):
	output_file(file_output)

	source = create_data_source(data)

	p = figure(title="File Data", tools=[HoverTool(
		tooltips=[
		("name","@method_name"),
		("complexity","@complexity")
		])])

	p.line(source=source, y='line_num',x='complexity', line_width=2)

	y_min = 0
	y_max = max(source.data['line_num'])
	p.y_range = Range1d(y_max,y_min)
	show(p)

def create_data_source(data):
	source = ColumnDataSource(data=dict(
		line_num = [int(x[0]) for x in data],
		complexity = [int(x[2]) for x in data],
		method_name = [x[1] for x in data]))
	return source

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("pyfile")
	parser.add_argument("--output", default="plot.html")
	args = parser.parse_args()
	main(args)