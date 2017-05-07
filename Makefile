log.log cpp.cpp: py.py
	python py.py > log.log && tail $(TAIL) log.log
