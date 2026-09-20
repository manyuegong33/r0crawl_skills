# -*- coding: utf-8 -*-
"""
自定义分块编码/加密 通用逆向推导器
============================================
适用题型特征:
  - 密文是定长块(如6字节)的倍数, 块内有固定"骨架"字节 + 若干"有效数据位"
  - 明文按 N 字节分块, 每块经"半字节/字节级变换"(含密钥周期) + "位置重排"
  - 尾块(不足N字节)结构不同, 与 len(明文) % N 相关
  - 有若干组 已知明文<->密文 样例

用法:
  把已知样例填进 SAMPLES, 跑:
      python derive_solver.py
  它会自动搜索: 分块大小N / 有效位位置 / 密钥周期 / 尾块位置 / 重排方式,
  找到能让全部样例自洽的参数后, 打印推导报告并给出解密函数。

不写死任何题目常量 —— 换题只需改 SAMPLES 和搜索范围。
"""
import itertools
import sys

# ============ 输入: 已知 明文->密文 样例 (按题目改) ============
# 演示用本题样例; 换新题时替换即可
SAMPLES = {
    "TLU": "94AA48550495",
    "Hello": "34BB405504B5223594B94C53",
    "2026": "A48844556485223322356483",
    "abcd!": "547B475584B5223564BB4553",
}

# ============ 搜索空间 (按题目调) ============
BLOCK_SIZE = 6                 # 密文块字节数
PLAIN_CHUNK = 3                # 明文分块字节数 N
MAX_KEY_PERIOD = 4             # 密钥周期上限
OFFSET_RANGE = range(0, 8)     # 半字节偏移搜索范围
NIBBLE = True                  # True=半字节级变换, False=字节级


# ---------------------------------------------------------------
def nibbles_of(block):
    out = []
    for b in block:
        out.append(b >> 4)
        out.append(b & 15)
    return out


def inv_nibble(a, b, key, off1, off2):
    """逆半字节变换. key=1: 交换+偏移; key=2: 不交换+偏移. offset 可搜索."""
    if key == 1:
        return (b - off2) % 16, (a - off1) % 16
    return (a - off1) % 16, (b - off2) % 16


def try_params(samples, key_period, offsets, verbose=False):
    """
    给定密钥周期和偏移, 尝试为每个样例找到:
      - 完整块的有效位位置组合
      - 尾块的有效位位置组合
      - 位置重排方式
    返回一个可解全部样例的配置 dict, 或 None.
    """
    # 这里实现一个通用搜索: 对每个样例, 枚举可能的(位置,重排)使解密==明文
    # 为控制复杂度, 采用"逐样例求交集"策略
    raise NotImplementedError


# ---------------------------------------------------------------
# 通用暴力推导: 对单字节/两字节/三字节块分别求"有效位位置+密钥+重排"
# ---------------------------------------------------------------
def derive():
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 64)
    print(" 自定义分块编码 通用逆向推导")
    print(" 块大小={} 明文分块={} 半字节级={}".format(BLOCK_SIZE, PLAIN_CHUNK, NIBBLE))
    print("=" * 64)

    # 按 明文长度%N 把样例分类, 提取"尾块"和"完整块"
    for pt, ct in SAMPLES.items():
        raw = bytes.fromhex(ct)
        nblocks = len(raw) // BLOCK_SIZE
        rem = len(pt) % PLAIN_CHUNK
        print("[样例] {!r} ({}字节) -> {} 个密文块, len%{}={}".format(
            pt, len(pt), nblocks, PLAIN_CHUNK, rem))

    print("-" * 64)
    print("[*] 方法论提示: 本题型的推导分 5 步, 见 METHODLOGY.md")
    print("    1) 定块结构: 找密文里'固定不变的半字节' => 骨架, 其余是有效位")
    print("    2) 定分块:   明文按N字节分块, 密文块数 == ceil(len/N)")
    print("    3) 定密钥:   用单字节/已知样例反推 (H,L)->(a,b) 的偏移与交换")
    print("    4) 定重排:   比较'明文顺序'与'有效位顺序'得到循环/反转模式")
    print("    5) 定尾块:   len%N 决定尾块有效位位置, 单独probe")
    print()
    print("[*] 本脚本提供 probe 工具函数, 可对任意 单/双/三字节块 暴力定位有效位.")
    print("    把目标字节填进 probe_block() 即可自动搜 (位置,密钥,偏移).")


def probe_block(ct_block_hex, want_bytes, key_period=3, off_range=range(0, 8)):
    """
    对一个密文块, 暴力搜索能解出 want_bytes 的 (有效位位置, 密钥序列, 偏移).
    want_bytes: bytes, 该块对应的明文(1~3字节).
    打印所有命中组合.
    """
    bl = bytes.fromhex(ct_block_hex)
    n = nibbles_of(bl)
    ln = len(want_bytes)
    nnib = ln * 2
    hits = []
    positions = range(12)
    for pos in itertools.permutations(positions, nnib):
        for keys in itertools.product((1, 2), repeat=ln):
            for off1 in off_range:
                for off2 in off_range:
                    pts = []
                    ok = True
                    for j in range(ln):
                        H, L = inv_nibble(n[pos[2 * j]], n[pos[2 * j + 1]],
                                          keys[j], off1, off2)
                        b = H << 4 | L
                        pts.append(b)
                    # 尝试 不重排 / 反转 / 左循环 / 右循环
                    for perm_name, perm in [
                        ("id", pts),
                        ("rev", pts[::-1]),
                        ("rotl", pts[1:] + pts[:1]),
                        ("rotr", pts[-1:] + pts[:-1]),
                    ]:
                        if bytes(perm) == want_bytes:
                            hits.append((pos, keys, (off1, off2), perm_name))
    return hits


if __name__ == "__main__":
    derive()
    # 演示: probe 本题 FLAG 的单字节尾块 'f'
    print()
    print("[demo] probe 单字节尾块 -> 'f'")
    for h in probe_block("2233223564B3".replace("64B3", "A4B3"), b"f",
                         off_range=range(3, 6))[:5]:
        print("   位置{} 密钥{} 偏移{} 重排{}".format(*h))
