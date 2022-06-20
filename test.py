from jsmpy import *
from utils import *
import pprint, re
code = """

print(12, 'nice, this is Amazing!')
print("ok ,'123'")

print("one", "two", 45.99, 3, [1,2,3], ["dd", "bb"], {"nice": 123}, var, {"ddff":456})

k = [1,2]
print(k)
function haha(){
	var = 6
	print("inside")
}


haha()

"""


parse_code = Parser(code)

# print(parse_code.find_blocks())
# print(parse_code.find_calls())
# print(parse_code.find_variables())

# for m in re.finditer(r"^([a-zA-Z0-9_ ]+)=([^\n]+)", code , re.MULTILINE | re.DOTALL):
	# print(m.groups())

pp = pprint.PrettyPrinter(width=41, compact=True)
pp.pprint(parse_code.parse())
parse_code.eval()
# pp.pprint(parse_code.ENV)

# a = parse_code.parse_var('[1,2,["ff"], true]')
# print(a, type(a))
# n, a = parse_code.parse()[0][2]
# n2, a2 = parse_code.parse()[1][2]
# print("-"*10)
# print(a, a2)

# print(parse_code.find_strings(a2))

# for m in re.finditer(r"'([^']*)'|\"([^\"]*)\"", a ):
	# print(m.groups())
# for m in re.finditer(r"'([^']*)'|\"([^\"]*)\"", a2 ):
	# print(m.groups())





# d = {'d': 13, 'math': {'f': 45, "haha":{"g":465}}}

# for k, v in getKeysDict(ENV):
	# print(k)


