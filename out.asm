jmp _func_is_prime_end
_func_is_prime:
push rbp
mov rbp, rsp
mov rax, 2
push rax
_start_cycle_1:
mov rax, [rbp - 8]
push rax
mov rax, [rbp + 16]
push rax
pop rbx
pop rcx
xor rax, rax
cmp rcx, rbx
setl al
cmp rax, 0
je _end_cycle_1
mov rax, [rbp + 16]
push rax
mov rax, [rbp - 8]
push rax
pop rbx
pop rax
cqo
idiv rbx
mov rax, rdx
push rax
mov rax, 0
push rax
pop rbx
pop rcx
xor rax, rax
cmp rcx, rbx
sete al
cmp rax, 0
je _else_2
mov rax, 0
jmp _func_is_prime_pre_end
jmp _post_cond_2
_else_2:
mov rax, [rbp - 8]
push rax
mov rax, 1
push rax
pop rax
pop rbx
add rax, rbx
mov [rbp - 8], rax
_post_cond_2:
jmp _start_cycle_1
_end_cycle_1:
mov rax, 1
jmp _func_is_prime_pre_end
_func_is_prime_pre_end:
mov rsp, rbp
pop rbp
ret 8
_func_is_prime_end:
jmp _func_main_end
_func_main:
push rbp
mov rbp, rsp
mov rax, 0
push rax
mov rax, [rbp + 16]
push rax
_start_cycle_3:
mov rax, [rbp - 16]
push rax
mov rax, [rbp + 24]
push rax
pop rbx
pop rcx
xor rax, rax
cmp rcx, rbx
setle al
cmp rax, 0
je _end_cycle_3
mov rax, [rbp - 16]
push rax
call _func_is_prime
cmp rax, 0
je _else_4
mov rax, [rbp - 8]
push rax
mov rax, [rbp - 16]
push rax
pop rax
pop rbx
add rax, rbx
mov [rbp - 8], rax
mov rax, [rbp - 16]
push rax
mov rax, 1
push rax
pop rax
pop rbx
add rax, rbx
mov [rbp - 16], rax
jmp _post_cond_4
_else_4:
mov rax, [rbp - 16]
push rax
mov rax, 1
push rax
pop rax
pop rbx
add rax, rbx
mov [rbp - 16], rax
_post_cond_4:
jmp _start_cycle_3
_end_cycle_3:
mov rax, [rbp - 8]
jmp _func_main_pre_end
_func_main_pre_end:
mov rsp, rbp
pop rbp
ret 16
_func_main_end:
push 0b10100
push 2
call _func_main