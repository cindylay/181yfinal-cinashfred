import infer_model
import re
escaped = r'"""' + "argument: a list, L \n returns: the sum of all elements in the list" + r'"""'

print(escaped)
print(infer_model.infer(prompt = escaped))