log.log: ./exe.exe
	./exe.exe >> $@ && tail $(TAIL) $@
./exe.exe: cpp.cpp
	$(CXX) -o $@ $^
cpp.cpp: py.py
	python py.py

