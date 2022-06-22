import re, math, inspect, requests, json, operator
from utils import *


#### TODO:

# add methods to calls. example: requests.get("something") --> requests.get("something").text ...
# replace calls with their return values. example: print(add(1,2)) --> print(3) --> 3
# look for blocks inside blocks
# eval blocks

#### Currently:

# every new call/variable... must be in a new line
# you can't use double quotes inside a double quote string, same thing as single quotes. (can be fixed with a better regex)
# you need to use double quotes inside a dictionary just like json.

def clear_modules(d):
	new_d = {}
	for k,v in d.items():
		if inspect.isfunction(v) or inspect.ismethod(v) or inspect.isbuiltin(v) or inspect.isroutine(v) or isinstance(v, (float, int, str, list, dict)):
			if not "__" in k:
				new_d[k] = v
	return new_d

ENV = {}
ENV.update({
	'add':operator.add, 'sub':operator.sub, 'mul':operator.mul, 'div':operator.truediv, 
	'gt':operator.gt, 'lt':operator.lt, 'ge':operator.ge, 'le':operator.le, 'eq':operator.eq, 
	'abs':     	abs,
	'len':		len, 
	'map':     	map,
	'max':     	max,
	'min':     	min,
	'print':   	print,
	'round':   	round,
	'range':	range,
	"type":		type,
	'requests.get':	requests.get
})

for dt in [float, int, str, list, dict]:
	for key, value in clear_modules(dict(vars(dt))).items():
		ENV.update({dt.__name__ + "." + key: value})
for key, value in clear_modules(vars(math)).items():
	ENV.update({"math."+key: value})

##str.__class__.__base__.__subclasses__()

#####
class Parser:

	def __init__(self, js):
		self.js = js
		self.ENV = ENV.copy()
		self.builtinBlocks = ["if", "else", "while", "for"]
		self.reservedWords = ["function"] + self.builtinBlocks + [k for (k,v) in getKeysDict(ENV)]
		self.errors = []
	
	def parse(self):
		tokens = []
		
		blocks = self.find_blocks()
		blockLimits = [b[0] for b in blocks]
				
		variables = self.find_variables()
		calls = self.find_calls()
		
		for block in blocks:
			name, args, content = block[2]

			name = name.replace("function", "").strip()
			args = args.split(",")
			variables_block = [[min(v[0]), "v", v[2]] for v in variables if between_tuple(v[0], block[0])]
			calls_block = [[min(c[0]), "c", c[2]] for c in calls if between_tuple(c[0], block[0])][1:]
			
			tokens.append([min(block[0]), name, args, sorted(variables_block+calls_block)])

		tokens.extend([[min(v[0]), "v", v[2]] for v in variables if not between_tuples(v[0], blockLimits)])
		tokens.extend([[min(c[0]), "c", c[2]] for c in calls if not between_tuples(c[0], blockLimits)])
				
		return sorted(tokens)
		
	def eval(self):
		
		for line in self.parse():
			if len(line) == 3: ##variables and calls
				if line[1] == "c":
					name, args = line[2]
					if name.startswith("__"):
						self.error(f"call {name} can't be started with __")
					elif name in self.ENV:
						__c__ = self.ENV[name]
						args = self.parse_args(args)
								
						__c__(*args)
					else:
						self.error(f"function {name} is not initialised")
				if line[1] == "v":
					left, right = line[2]
					self.ENV[left.strip()] = self.parse_var(right)
			if len(line) > 3: ##blocks
				"""TODO"""
				pass
	
	def error(self, err):
		self.errors.append(err)
		print("Error:", err)
	
	def filter_regex(self, pattern, text):
		to_send = []
		
		for m in re.finditer(pattern, text, re.MULTILINE | re.DOTALL):
			to_send.append([m.span(), m.group(), m.groups()])
		
		return to_send
		
	def find_blocks(self):
		"if,else,while,for+functions"
		blocks_re = r"([a-zA-Z0-9_ ]*)\(([^\n]*)\){(.*?)}" ##three groups: name;parentheses;brackets
		
		return self.filter_regex(blocks_re, self.js)
	
	def find_variables(self):
		variables_re = r"^([a-zA-Z0-9_ \t]+)=([^\n]+)"
		
		return self.filter_regex(variables_re, self.js)
	
	def find_calls(self):
		"for every block, find their calls."
		calls_re = r"^([a-zA-Z0-9_ \.\t]*?)\(([^\n]*)\)"
		
		return self.filter_regex(calls_re, self.js)
	
	def parse_var(self, var):
		temp_var = var
		arr = re.findall(r"\[(.*?)\]|{(.*?)}", var)
		string = re.findall(r"'([^']*)'|\"([^\"]*)\"", var)
		
		try:
			var = int(var) ##if int
		except:
			try: ## it's a call
				name, args = re.findall(r"^([a-zA-Z0-9_ \.\t]*?)\(([^\n]*)\)", var)[0]
				if name.startswith("__"):
					self.error(f"call {name} can't be started with __")
				elif name.strip() in self.ENV:
					__call__ = self.ENV[name.strip()]
					var = __call__(*self.parse_args(args))
			except Exception as e:
				try:
					if "object is not callable" in str(e):
						name, args = re.findall(r"^([a-zA-Z0-9_ \.\t]*?)\(([^\n]*)\)", var)[0]
						var = self.ENV[name.strip()]
				except:
					pass
				# print(e)
				pass
		
		if var == temp_var:
			if arr:
				try:
					var = json.loads(var)
				except Exception as e:
					self.error(f"can't parse {var}")
			elif string:
				a, b = string[0]
				var = a if a else b
		
		if var == temp_var: ## if nothing else worked. maybe it's a variable in ENV.
			try:
				var = self.ENV[var.strip()]
			except:
				pass
		
		return var
	def parse_args(self, args):		
		##lists and dicts
		arrays = re.findall(r"\[(.*?)\]|{(.*?)}", args)
		aaa = []
		for arr in arrays:
			a, b = arr
			if a:
				aaa.append(f"[{a}]")
			elif b:
				aaa.append("{dict}".replace("dict", b))
		for i, s in enumerate(aaa):
			args = args.replace(s, f"[{i}]")
		
		
		##strings
		sss = []
		strings = re.findall(r"'([^']*)'|\"([^\"]*)\"", args)
		for s in strings:
			a, b = s
			if a:
				sss.append(a)
			elif b:
				sss.append(b)
		for i, s in enumerate(sss):
			args = args.replace(s, f"[{i+len(aaa)}]")
		
		##parsing them both
		aaasss = aaa+sss
		args = args.split(",")
		
		for arg in args:
			if not arg:
				self.error("one of the args is empty")
		
		listanddicts = [] ##indexes in args
		for i, a in enumerate(aaasss):
			for j, a_t in enumerate(args):
				if f"[{i}]" in a_t:
					try:
						args[j] = json.loads(a) ###parse lists and dicts
						listanddicts.append(j)
					except Exception as e:
						args[j] = a ## leave strings as written
						listanddicts.append(j)
		
		intsandfloats = [] ##indexes in args
		for i in range(len(args)):
			if not i in listanddicts:
				try:
					args[i] = json.loads(args[i]) ##parse floats and ints
					intsandfloats.append(i)
				except Exception as e:
					pass
		
		
		for i, arg in enumerate(args):
			if not arg in sss and not i in intsandfloats+listanddicts: ## if it is not a string/array, then it's a variable
				try:
					args[i] = self.ENV[args[i].strip()]
				except:
					self.error(f"variable: {args[i].strip()} is not initialised.")
		
		return args
