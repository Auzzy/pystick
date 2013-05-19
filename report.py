#from inv_util import Undef
from daikon.invariants.inv_util import Undef

def print_return_types(return_types):
	for return_type in return_types:
		print return_type

def print_funcs(builtins):
	for arg_num in builtins:
		for func_type in builtins[arg_num]:
			print "{0} {1}".format(arg_num,func_type).title()
			for func in sorted(builtins[arg_num][func_type], key=lambda afunc: afunc.__name__):
				for arg_names in sorted(builtins[arg_num][func_type][func]):
					args = ",".join(arg_names) if func_type=="const" else ",".join(arg_names[:-1])
					retval = builtins[arg_num][func_type][func][arg_names]
					print "{0}({1}) = {2}".format(func.__name__,args,retval)
			if arg_num!=builtins.keys()[-1] or func_type!=builtins[arg_num].keys()[-1]:
				print

def print_ordering(ordering):
	for var in sorted(ordering):
		for op in ordering[var]:
			print "{0} {1} {2}".format(var,op,",".join(ordering[var][op]))

def print_ranges(ranges):
	undef = []
	for var in sorted(ranges):
		var_range = ranges[var]
		if type(var_range) is Undef:
			undef.append(var)
		else:
			print str(var_range)
	if undef:
		print "Undefined: {0}".format(", ".join(undef))

invariants = ["variable ranges","variable ordering","builtin functions","return types"]
print_invariants = {"variable ranges": print_ranges,
		    "variable ordering": print_ordering,
		    "builtin functions": print_funcs,
		    "return types": print_return_types}


def sort_labels(labels):
	enter,exit,loop = [],[],[]
	for label in labels:
		if "Enter" in label:
			enter.append(label)
		if "Exit" in label:
			exit.append(label)
		if "Loop" in label:
			loop.append(label)
	return enter + sorted(loop) + sorted(exit)

def print_results(results):
	print
	label_names = sort_labels(results.keys())
	for label in label_names:
		print "{0}, line {1}".format(label[0],label[1]).upper()
		for invariant in invariants:
			if invariant in results[label]:
				if results[label][invariant]:
					print invariant.upper()
					print_invariants[invariant](results[label][invariant])
					print
		print
