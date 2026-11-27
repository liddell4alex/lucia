CXX = gcc
CXXFLAGS = -Wall -I./include

TARGET = ./build/lucia
SOURCES = ./src/engine.c ./src/matrix.c main.c

all:
	mkdir -p build && $(CXX) $(CXXFLAGS) $(SOURCES) -o $(TARGET)

clean:
	rm -f $(TARGET)
