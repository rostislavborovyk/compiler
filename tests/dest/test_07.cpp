#include <iostream>
#include <string>
#include <stdint.h>
using namespace std;
int main()
{
	int b;
  	asm (

	"jmp _func_main_end;"
	"_func_main:;"
	"push rbp;"
	"mov rbp, rsp;"
	"mov rax, 100;"
	"push rax;"
	"mov rax, 10;"
	"push rax;"
	"pop rax;"
	"pop rbx;"
	"add rax, rbx;"
	"push rax;"
	"mov rax, 12;"
	"push rax;"
	"pop rbx;"
	"pop rax;"
	"sub rax, rbx;"
	"push rax;"
	"mov rax, 14;"
	"push rax;"
	"mov rax, 2;"
	"push rax;"
	"pop rbx;"
	"pop rax;"
	"cqo;"
	"idiv rbx;"
	"push rax;"
	"pop rax;"
	"pop rbx;"
	"add rax, rbx;"
	"push rax;"
	"mov rax, 10;"
	"neg rax;"
	"push rax;"
	"mov rax, 3;"
	"push rax;"
	"pop rax;"
	"pop rbx;"
	"xor rdx, rdx;"
	"cqo;"
	"imul rbx;"
	"push rax;"
	"pop rbx;"
	"pop rax;"
	"sub rax, rbx;"
	"jmp _func_main_pre_end;"
	"_func_main_pre_end:;"
	"mov rsp, rbp;"
	"pop rbp;"
	"ret ;"
	"_func_main_end:;"
	"call _func_main;"

  		 : "=r" ( b )
  		 );
	cout << b << endl;
	return 0;
}
