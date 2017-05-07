log.log: ./exe.exe
	./exe.exe >> $@ && tail $(TAIL) $@
cpp.cpp: py.py
	python py.py > log.log && tail $(TAIL) $@
./exe.exe: cpp.cpp
	$(CXX) -o $@ $^
