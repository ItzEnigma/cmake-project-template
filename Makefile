prepare:
	rm -rf build
	mkdir build
	cd build && cmake ..

build:
	cd build && cmake --build . --config Release

run:
	./build/${EXECUTABLE_NAME}