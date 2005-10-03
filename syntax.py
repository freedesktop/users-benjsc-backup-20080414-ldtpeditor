import tokenize
import keyword
import __builtin__

class PythonSyntax:
    def scan (self, code):
	self.code = code
	self.position = 0
	self.prev = None 
	self.curr = None 
	
	try:
		for type, text, (srow, scol), (erow, ecol), line in \
			tokenize.generate_tokens (self.readline):
			  
			self.prev = self.curr
			self.curr = text
	
			tag = None
		
			if type == tokenize.NAME: 
				if keyword.iskeyword (text):
					tag = "python_keyword"
				elif text in dir (__builtin__):
					tag = "python_builtin"
				elif self.prev == "def" or self.prev == "class":
					tag = "python_function"
	
			elif type == tokenize.STRING:
				tag = "python_string"
			
			elif type == tokenize.NUMBER:
				tag = "python_string"
	
			elif type == tokenize.COMMENT:
				ecol = ecol-1
				tag = "python_comment"
	
			if tag:
				yield tag, (srow, scol), (erow, ecol)

	except tokenize.TokenError, e:
		pass

    def readline (self):
	if self.position < len (self.code):
		index = self.code.find ('\n', self.position)
		if index != -1:
			line = self.code[self.position:index] + '\n'
			self.position = index + 1
		else:
			line = self.code[self.position:] + '\n'
			self.position = len (self.code)
	else:
		line = ''

	return line

