"""
from pystick.daikon.logging import log
from pystick.daikon.invariants import detect
"""
from logging import log
from invariants import detect

def select_inputs(input_groups):
	selected = set()
	for inputs in input_groups:
		selected.update(input_groups[inputs])
	return list(selected)

def run(program_text, func, input_groups):
	input_list = select_inputs(input_groups)
	traces = log(program_text,func,input_list)
	return detect(traces)
