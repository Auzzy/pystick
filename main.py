from imp import load_source as load_module
from os.path import basename,splitext

from dart import run as run_DART
from daikon import run as run_Daikon

from report import print_results

def run(file_name, func_name):
	program_text = open(file_name,'r').read()
	user_mod = load_module(splitext(basename(file_name))[0],file_name)
	user_func = getattr(user_mod,func_name)

	input_dict = run_DART(program_text,user_func)
	results = run_Daikon(program_text,user_func,input_dict)

	print
	print

	print_results(results)

if __name__=="__main__":
	from sys import argv
	run(argv[1],argv[2])
