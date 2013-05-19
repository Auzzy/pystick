from numbers import Number
from itertools import combinations as comb, permutations as perm

from inv_util import *

if __package__=="pystick":
	from pystick.commonast import *
	from pystick.util import *
else:
	import sys
	from os.path import abspath, dirname, pardir, join as path_join
	sys.path.append(abspath(path_join(dirname(__file__),pardir,pardir)))
	from commonast import *
	from util import *

comp_ops = {"lt": "<",
	    "le": "<=",
	    "gt": ">",
	    "ge": ">=",
	    "eq": "==",
	    "ne": "!="}
traces = {}
vars = []
funcs = {"unary": {"const": [bin,bool,chr,hex,oct,unichr],
		   "var": [abs]},
	 "binary": {"const": [cmp,divmod,pow],
		    "var": [cmp,divmod,pow]}}

def update_results(var_results, result, retval_name, retval):
	for func in result:
		if func in var_results:
			if result[func]!=retval:
				del var_results[func]
		else:
			var_results[func] = retval_name

def detect_var_funcs(section, inputs, all_var_funcs):
	results = {}
	for arg_names in inputs:
		var_funcs = all_var_funcs
		results[arg_names] = {}
		for trace in section:
			args = [trace[var] for var in arg_names if isinstance(trace[var],Number)]
			if len(args)==len(arg_names):
				result_dict = run_funcs(var_funcs,args[:-1])
				update_results(results[arg_names],result_dict,arg_names[-1],args[-1])
				var_funcs = results[arg_names].keys()
			else:
				results[arg_names] = {}
				break
	
	return results

def update_const_results(var_results, result):
	for func in result:
		if func in var_results:
			if result[func]!=var_results[func]:
				del var_results[func]
		else:
			var_results[func] = result[func]

def detect_const_funcs(section, inputs, all_const_funcs):
	results = {}
	for arg_names in inputs:
		const_funcs = all_const_funcs
		results[arg_names] = {}
		for trace in section:
			args = [trace[var] for var in arg_names if isinstance(trace[var],Number)]
			if len(args)==len(arg_names):
				result_dict = run_funcs(const_funcs,args)
				update_const_results(results[arg_names],result_dict)
				const_funcs = results[arg_names].keys()
			else:
				results[arg_names] = {}
				break
	
	return results

def detect_binary_funcs(section):
	return detect_var_funcs(section,perm(vars,3),funcs["binary"]["var"])

def detect_unary_funcs(section):
	return detect_var_funcs(section,perm(vars,2),funcs["unary"]["var"])

def detect_binary_const_funcs(section):
	return detect_const_funcs(section,perm(vars,2),funcs["binary"]["const"])

def detect_unary_const_funcs(section):
	return detect_const_funcs(section,perm(vars,1),funcs["unary"]["const"])

def invert_results(results):
	inverted_results = {}
	for arg_names in results:
		for func in results[arg_names]:
			if func not in inverted_results:
				inverted_results[func] = {}
			inverted_results[func][arg_names] = results[arg_names][func]
	return inverted_results

def detect_funcs(section):
	results = {}

	unary_const = invert_results(detect_unary_const_funcs(section))
	unary_var = invert_results(detect_unary_funcs(section))
	binary_const = invert_results(detect_binary_const_funcs(section))
	binary_var = invert_results(detect_binary_funcs(section))

	if unary_const or unary_var:
		results["unary"] = {}
		if unary_const:
			results["unary"]["const"] = unary_const
		if unary_var:
			results["unary"]["var"] = unary_var
	if binary_const or binary_var:
		results["binary"] = {}
		if binary_const:
			results["binary"]["const"] = binary_const
		if binary_var:
			results["binary"]["var"] = binary_var
	
	return results


def compare(order, var1, var2):
	if order["eq"]:
		return "eq"
	elif order["le"]:
		return "lt" if order["lt"] else "le"
	elif order["ge"]:
		return "gt" if order["gt"] else "ge"
	elif order["ne"]:
		return "ne"

def compare_values(val1, val2):
	return {"lt": val1<val2,
		"le": val1<=val2,
		"gt": val1>val2,
		"ge": val1>=val2,
		"eq": val1==val2,
		"ne": val1!=val2}

def var_order(var1, var2, section):
	order = dict.fromkeys(comp_ops.keys(),True)
	for trace in section:
		val1,val2 = trace[var1],trace[var2]
		if isinstance(val1,Number) and isinstance(val2,Number):
			comp = compare_values(val1,val2)
			order = {op:order[op] and comp[op] for op in comp}
		else:
			return None
	
	return compare(order,var1,var2)

def detect_ordering(section):
	ordering = {}
	for var1,var2 in comb(vars,2):
		order = var_order(var1,var2,section)
		if order:
			if var1 not in ordering:
				ordering[var1] = {}
			if comp_ops[order] not in ordering[var1]:
				ordering[var1][comp_ops[order]] = []
			ordering[var1][comp_ops[order]].append(var2)
	
	return ordering


def get_range(section, var):
	vals = [trace[var] for trace in section if isinstance(trace[var],Number)]

	if vals:
		min_val,max_val = min(vals),max(vals)
		return Const(var,min_val) if min_val==max_val else Range(var,min_val,max_val)
	else:
		return Undef(var)

def detect_ranges(section):
	ranges = {}
	for var in vars:
		ranges[var] = get_range(section,var)
		#print str(ranges[var])
	return ranges


def detect_return(section):
	return_types = list({trace["return"] for trace in section if "return" in trace})
	return return_types 


def generate_traces(trace_list):
	global traces,label_names,vars
	labels = trace_list[0].keys()
	traces = {label:[] for label in labels}
	
	for trace in trace_list:
		for label in trace:
			traces[label].append(trace[label])
	
	vars = sorted(traces[labels[0]][0].keys())
	if "return" in vars:
		vars.remove("return")

def detect(trace_list):
	generate_traces(trace_list)

	results = {}
	for label in traces:
		section = traces[label]

		results[label] = {}
		results[label]["return types"] = detect_return(section)
		results[label]["variable ranges"] = detect_ranges(section)
		results[label]["variable ordering"] = detect_ordering(section)
		results[label]["builtin functions"] = detect_funcs(section)
	
	return results
