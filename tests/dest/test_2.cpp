#include <iostream>
#include <string>
#include <stdint.h>
using namespace std;
int main()
{
	int b;
  	asm (

	"xor rdx, rdx;"
	"push rbp;"
	"mov rbp, rsp;"
	"mov rax, 4;"
	"neg rax;"
	"push rax;"
	"mov rax, 2;"
	"push rax;"
	"mov rax, [rbp - 8];"
	"push rax;"
	"mov rax, [rbp - 16];"
	"push rax;"
	"pop rbx;"
	"pop rax;"
	"idiv rbx;"
	"mov rsp, rbp;"
	"pop rbp;"
  		 : "=r" ( b )
  		 );
	cout << b << endl;
	return 0;
}
