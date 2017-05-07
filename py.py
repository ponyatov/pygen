log = open('log.log','w')
cpp = open('cpp.cpp','w')
print >>cpp,'// autogen: https://github.com/ponyatov/pygen'

class AST:
	# constructor
	def __init__(self,V):
		self.tag = self.__class__.__name__ ; self.val = V
		self.nest = [] ; self.attr = {}
	# dump
	def __repr__(self): return self.dump()
	def dump(self,depth=0,prefix=''):
		S = '\n'+'\t'*depth + prefix + self.head()
		for i in self.attr: S += self.attr[i].dump(depth+1,prefix='%s = '%i)
		for j in self.nest: S += j.dump(depth+1)
		return S
	def head(self): return '<%s:%s>'%(self.tag,self.val)
	# operators
	def __div__(self,o): self.nest.append(o) ; return self
	def __getitem__(self,K): return self.attr[K]
	def __setitem__(self,K,V): self.attr[K] = V ; return self
	# codegen
	def cpp(self,depth=0):
		C = '\t'*depth+'// %s\n\n'%self.head()
		for j in self.nest: C += j.cpp(depth+1)
		return C

class Program(AST): pass

class Scalar(AST):
	def cpp(self): return self.val
class Symbol(Scalar): pass
class Integer(Scalar): pass

class Vector(AST):
	def __init__(self): AST.__init__(self,'[]')
	def cpp(self,depth=0):
		C = ''
		for j in self.nest: C += j.cpp()
		return C

class Type(Symbol):
	def __init__(self,*args):
		Symbol.__init__(self,self.__class__.__name__.lower())
		for i in args:
			if type(i) == str: self/Symbol(i)
			else: self/i
	def cpp(self,depth=0):
		C = self.val
		if self.nest: C += ' '+self.nest[0].cpp()
		return C
	def ret(self,X,depth=0):
		return '\t'*depth+'return (%s)(%s);\n'%(self.cpp(),X.cpp())
class Int(Type): pass
int = Int()
class Void(Type): pass
void = Void()
class Char(Type): pass
char = Char()

class Ptr(Type):
	def cpp(self,depth=0): return '*%s'%self.nest[0].cpp()
class Array(Type):
	def cpp(self,depth=0): return '%s[]'%self.nest[0].cpp()

class Arg(Vector):
	def cpp(self,depth=0):
		C = ''
		for j in self.nest: C += j.cpp()+', '
		return C[:-2]


class Function(AST):
	def __init__(self,R,V,A):
		AST.__init__(self,V) ; self['type'] = R ; self['arg'] = A
	def cpp(self,depth=0):
		C = '%s %s(%s) {\n'%(self['type'].cpp(),self.val,self['arg'].cpp())
		for j in self.nest: C += j.cpp(depth+1)
		C += self['type'].ret(Integer(0),depth)
		return C+'}\n\n'

prog = Program('Hello') \
/ Function(int,'main',Arg()/Int('argc')/Char(Ptr(Array('argv'))))

print >>log,prog
print >>cpp,prog.cpp()

