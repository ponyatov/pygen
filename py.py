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
	# codegen
	def cpp(self):
		C = '// %s\nint main(){}\n'%self.head()
		for j in self.nest: C += j.cpp()
		return C

class Program(AST): pass

prog = Program('Hello')

print >>log,prog
print >>cpp,prog.cpp()

