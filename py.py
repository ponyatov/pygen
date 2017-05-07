log = open('log.log','w')
cpp = open('cpp.cpp','w')
print >>cpp,'// autogen: https://github.com/ponyatov/pygen'

class AST:
	# constructor
	def __init__(self,V):
		self.tag = self.__class__.__name__ ; self.val = V
		self.nest = []
	# dump
	def __repr__(self): return self.dump()
	def dump(self,depth=0):
		S = '\n'+'\t'*depth+self.head()
		for j in self.nest: S += j.dump(depth+1)
		return S
	def head(self): return '<%s:%s>'%(self.tag,self.val)
	# operators
	def __div__(self,o): self.nest.append(o) ; return self
	# codegen
	def cpp(self):
		C = '// %s\n\n'%self.head()
		for j in self.nest: C += j.cpp()
		return C

class Program(AST): pass

class Function(AST):
	def cpp(self): return 'int %s(){}\n'%self.val

prog = Program('Hello') \
/ Function('main')

print >>log,prog
print >>cpp,prog.cpp()

