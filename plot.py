import csv
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool, LabelSet, Label

def main(args):
	with open(args.input) as f:
		file_data = list(csv.reader(f))
	plot(file_data,args.output)


def plot(data,file_output):
	output_file(file_output)

	source = create_data_source(data)

	p = figure(title="File Data", tools=[HoverTool(
		tooltips=[
		("name","@method_name")])])
	

	p.line(source=source, x='line_num',y='complexity', line_width=2)
	
	labels = LabelSet(x='line_num', y='complexity', text='method_name', level='glyph',
              x_offset=5, y_offset=5, source=source, render_mode='canvas')

	# p.add_layout(labels)

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
	parser.add_argument("input")
	parser.add_argument("--output", default="plot.html")
	args = parser.parse_args()
	main(args)