# IDAPython starter: export named functions and addresses.
import ida_funcs, ida_name, idaapi
for ea in ida_funcs.Functions():
    name=ida_name.get_name(ea) or idaapi.get_name(ea)
    print(f"0x{ea:x}\t{name}")
