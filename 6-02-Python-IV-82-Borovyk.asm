jmp _func_main_end
_func_main:
push ebp
mov ebp, esp
mov eax, 1
push eax
mov eax, 2
push eax
pop ebx
pop eax
cmp eax, ebx
setne al
jmp _func_main_pre_end
_func_main_pre_end:
mov esp, ebp
pop ebp
ret 
_func_main_end:
call _func_main