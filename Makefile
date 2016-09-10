hellworld:file1.o
	gcc file1.o -o helloworld
file1.o:file1.c
	gcc -c file1.c -o file1.o
clean:
	rm -rf *.o helloworld

