from copy import deepcopy

__env_dict = {}

def __env_update(start, end):
	__env_dict[start] = __env_find_scope(start)
	for lineno in range(start,end):
		if __env_dict[lineno] is not None:
			__env_dict[lineno+1] = deepcopy(__env_dict[lineno])

def __env_find_scope(start):
	linenos = sorted(__env_dict.keys())
	if start in linenos:
		del linenos[linenos.index(start):]
	return deepcopy(__env_dict[linenos[-1]])

def __env_init_loop(loop_start):
	__env_dict[loop_start] = {}
	__env_dict[loop_start][1] = deepcopy(__env_dict[loop_start-1])

def __env_update_loop(start, end, loop_start, loop_end, iter_num):
	state = __env_find_scope_loop(start,loop_start,loop_end)
	if start not in __env_dict:
		__env_dict[start] = {}
	
	__env_dict[start][iter_num] = deepcopy(state)

	for lineno in range(start,end):
		if __env_dict[lineno] is not None:
			if lineno+1 not in __env_dict:
				__env_dict[lineno+1] = {}
			__env_dict[lineno+1][iter_num] = deepcopy(state)

def __env_find_scope_loop(lineno, loop_start, loop_end):
	if lineno==loop_start:
		if loop_start in __env_dict and __env_dict[loop_start]:
			max_iter_num = max(__env_dict[loop_start].keys())
			last_iter = deepcopy(__env_dict[loop_start][max_iter_num])
			if loop_end-1 in __env_dict:
				last_iter.update(deepcopy(__env_dict[loop_end-1][max_iter_num]))
			return last_iter
		else:
			return deepcopy(__env_dict[loop_start-1])
	else:
		max_iter_num = max(__env_dict[loop_start].keys())
		last_iter = deepcopy(__env_dict[lineno][max_iter_num-1]) if lineno in __env_dict else {}
		last_iter.update(deepcopy(__env_dict[lineno-1][max_iter_num]))
		return last_iter
	
def __env_cleanup_loop(lineno, start, end):
	scope = {}
	#if 1 in __env_dict[lineno].keys()[0]:
	for iter_num in sorted(__env_dict[lineno].keys()):
		scope.update(deepcopy(__env_dict[lineno][iter_num]))
	del __env_dict[lineno]
	__env_dict[lineno] = scope

def __env_complete_scope(start, end):
	for lineno in range(start,end+1):
		if lineno not in __env_dict:
			__env_dict[lineno] = None
