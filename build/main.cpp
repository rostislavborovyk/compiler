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
	"mov rax, 1;"
	"push rax;"
	"mov rax, 4;"
	"push rax;"
	"_start_cycle_1:;"
	"mov rax, [rbp - 16];"
	"cmp rax, 0;"
	"je _end_cycle_1;"
	"mov rax, [rbp - 16];"
	"push rax;"
	"mov rax, 2;"
	"push rax;"
	"pop rbx;"
	"pop rax;"
	"sub rax, rbx;"
	"cmp rax, 0;"
	"je _else_2;"
	"mov rax, [rbp - 8];"
	"push rax;"
	"mov rax, 2;"
	"push rax;"
	"pop rax;"
	"pop rbx;"
	"xor rdx, rdx;"
	"cqo;"
	"imul rbx;"
	"mov [rbp - 8], rax;"
	"jmp _post_cond_2;"
	"_else_2:;"
	"mov rax, [rbp - 16];"
	"push rax;"
	"mov rax, 1;"
	"push rax;"
	"pop rbx;"
	"pop rax;"
	"sub rax, rbx;"
	"mov [rbp - 16], rax;"
	"jmp _start_cycle_1;"
	"_post_cond_2:;"
	"mov rax, [rbp - 16];"
	"push rax;"
	"mov rax, 1;"
	"push rax;"
	"pop rbx;"
	"pop rax;"
	"sub rax, rbx;"
	"mov [rbp - 16], rax;"
	"jmp _start_cycle_1;"
	"_end_cycle_1:;"
	"mov rax, [rbp - 8];"
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
