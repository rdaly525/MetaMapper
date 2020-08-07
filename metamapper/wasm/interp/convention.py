i32 = 0x7f
i64 = 0x7e
f32 = 0x7d
f64 = 0x7c

valtype = {
    i32: ['i32'],
    i64: ['i64'],
    f32: ['f32'],
    f64: ['f64'],
}

empty = 0x40

blocktype = {
    empty: ['empty'],
    **valtype
}

funcref = 0x70

elemtype = {
    funcref: ['funcref'],
}


opcodes = {}

def op_name(code):
    assert code in opcodes
    return opcodes[code][0]

def op(code, name, code_size, load_size):
    opcodes[code] = (name, code_size, load_size)
    return code

#Added by ross
i32_arg = op(-1,'i32.arg','',0)

# control Instructions
unreachable = op(0x00, 'unreachable', '', 0)
nop = op(0x01, 'nop', '', 0)
block = op(0x02, 'block', 'u8', 0)
loop = op(0x03, 'loop', 'u8', 0)
if_ = op(0x04, 'if', 'u8', 0)
else_ = op(0x05, 'else', '', 0)
end = op(0x0b, 'end', '', 0)
br = op(0x0c, 'br', 'u32', 0)
br_if = op(0x0d, 'br_if', 'u32', 0)
br_table = op(0x0e, 'br_table', 'complex', 0)
return_ = op(0x0f, 'return', '', 0)
call = op(0x10, 'call', 'u32', 0)
call_indirect = op(0x11, 'call_indirect', 'u32,u8', 0)
# parametric Instructions
drop = op(0x1a, 'drop', '', 0)
select = op(0x1b, 'select', '', 0)
# variable instructions
get_local = op(0x20, 'local.get', 'u32', 0)
set_local = op(0x21, 'local.set', 'u32', 0)
tee_local = op(0x22, 'local.tee', 'u32', 0)
get_global = op(0x23, 'global.get', 'u32', 0)
set_global = op(0x24, 'global.set', 'u32', 0)
# memory instructions
i32_load = op(0x28, 'i32.load', 'u32,u32', 4)
i64_load = op(0x29, 'i64.load', 'u32,u32', 8)
f32_load = op(0x2a, 'f32.load', 'u32,u32', 4)
f64_load = op(0x2b, 'f64.load', 'u32,u32', 8)
i32_load8_s = op(0x2c, 'i32.load8_s', 'u32,u32', 1)
i32_load8_u = op(0x2d, 'i32.load8_u', 'u32,u32', 1)
i32_load16_s = op(0x2e, 'i32.load16_s', 'u32,u32', 2)
i32_load16_u = op(0x2f, 'i32.load16_u', 'u32,u32', 2)
i64_load8_s = op(0x30, 'i64.load8_s', 'u32,u32', 1)
i64_load8_u = op(0x31, 'i64.load8_u', 'u32,u32', 1)
i64_load16_s = op(0x32, 'i64.load16_s', 'u32,u32', 2)
i64_load16_u = op(0x33, 'i64.load16_u', 'u32,u32', 2)
i64_load32_s = op(0x34, 'i64.load32_s', 'u32,u32', 4)
i64_load32_u = op(0x35, 'i64.load32_u', 'u32,u32', 4)
i32_store = op(0x36, 'i32.store', 'u32,u32', 4)
i64_store = op(0x37, 'i64.store', 'u32,u32', 8)
f32_store = op(0x38, 'f32.store', 'u32,u32', 4)
f64_store = op(0x39, 'f64.store', 'u32,u32', 8)
i32_store8 = op(0x3a, 'i32.store8', 'u32,u32', 1)
i32_store16 = op(0x3b, 'i32.store16', 'u32,u32', 2)
i64_store8 = op(0x3c, 'i64.store8', 'u32,u32', 1)
i64_store16 = op(0x3d, 'i64.store16', 'u32,u32', 2)
i64_store32 = op(0x3e, 'i64.store32', 'u32,u32', 4)
current_memory = op(0x3f, 'memory.size', 'u8', 0)
grow_memory = op(0x40, 'memory.grow', 'u8', 1)
# numeric instructions
i32_const = op(0x41, 'i32.const', 'i32', 2)
i64_const = op(0x42, 'i64.const', 'i64', 1)
f32_const = op(0x43, 'f32.const', 'f32', 2)
f64_const = op(0x44, 'f64.const', 'f64', 4)
i32_eqz = op(0x45, 'i32.eqz', '', 0)
i32_eq = op(0x46, 'i32.eq', '', 0)
i32_ne = op(0x47, 'i32.ne', '', 0)
i32_lt_s = op(0x48, 'i32.lt_s', '', 0)
i32_lt_u = op(0x49, 'i32.lt_u', '', 0)
i32_gt_s = op(0x4a, 'i32.gt_s', '', 0)
i32_gt_u = op(0x4b, 'i32.gt_u', '', 0)
i32_le_s = op(0x4c, 'i32.le_s', '', 0)
i32_le_u = op(0x4d, 'i32.le_u', '', 0)
i32_ge_s = op(0x4e, 'i32.ge_s', '', 0)
i32_ge_u = op(0x4f, 'i32.ge_u', '', 0)
i64_eqz = op(0x50, 'i64.eqz', '', 0)
i64_eq = op(0x51, 'i64.eq', '', 0)
i64_ne = op(0x52, 'i64.ne', '', 0)
i64_lt_s = op(0x53, 'i64.lt_s', '', 0)
i64_lt_u = op(0x54, 'i64.lt_u', '', 0)
i64_gt_s = op(0x55, 'i64.gt_s', '', 0)
i64_gt_u = op(0x56, 'i64.gt_u', '', 0)
i64_le_s = op(0x57, 'i64.le_s', '', 0)
i64_le_u = op(0x58, 'i64.le_u', '', 0)
i64_ge_s = op(0x59, 'i64.ge_s', '', 0)
i64_ge_u = op(0x5a, 'i64.ge_u', '', 0)
f32_eq = op(0x5b, 'f32.eq', '', 0)
f32_ne = op(0x5c, 'f32.ne', '', 0)
f32_lt = op(0x5d, 'f32.lt', '', 0)
f32_gt = op(0x5e, 'f32.gt', '', 0)
f32_le = op(0x5f, 'f32.le', '', 0)
f32_ge = op(0x60, 'f32.ge', '', 0)
f64_eq = op(0x61, 'f64.eq', '', 0)
f64_ne = op(0x62, 'f64.ne', '', 0)
f64_lt = op(0x63, 'f64.lt', '', 0)
f64_gt = op(0x64, 'f64.gt', '', 0)
f64_le = op(0x65, 'f64.le', '', 0)
f64_ge = op(0x66, 'f64.ge', '', 0)
i32_clz = op(0x67, 'i32.clz', '', 0)
i32_ctz = op(0x68, 'i32.ctz', '', 0)
i32_popcnt = op(0x69, 'i32.popcnt', '', 0)
i32_add = op(0x6a, 'i32.add', '', 0)
i32_sub = op(0x6b, 'i32.sub', '', 0)
i32_mul = op(0x6c, 'i32.mul', '', 0)
i32_div_s = op(0x6d, 'i32.div_s', '', 0)
i32_div_u = op(0x6e, 'i32.div_u', '', 0)
i32_rem_s = op(0x6f, 'i32.rem_s', '', 0)
i32_rem_u = op(0x70, 'i32.rem_u', '', 0)
i32_and = op(0x71, 'i32.and', '', 0)
i32_or = op(0x72, 'i32.or', '', 0)
i32_xor = op(0x73, 'i32.xor', '', 0)
i32_shl = op(0x74, 'i32.shl', '', 0)
i32_shr_s = op(0x75, 'i32.shr_s', '', 0)
i32_shr_u = op(0x76, 'i32.shr_u', '', 0)
i32_rotl = op(0x77, 'i32.rotl', '', 0)
i32_rotr = op(0x78, 'i32.rotr', '', 0)
i64_clz = op(0x79, 'i64.clz', '', 0)
i64_ctz = op(0x7a, 'i64.ctz', '', 0)
i64_popcnt = op(0x7b, 'i64.popcnt', '', 0)
i64_add = op(0x7c, 'i64.add', '', 0)
i64_sub = op(0x7d, 'i64.sub', '', 0)
i64_mul = op(0x7e, 'i64.mul', '', 0)
i64_div_s = op(0x7f, 'i64.div_s', '', 0)
i64_div_u = op(0x80, 'i64.div_u', '', 0)
i64_rem_s = op(0x81, 'i64.rem_s', '', 0)
i64_rem_u = op(0x82, 'i64.rem_u', '', 0)
i64_and = op(0x83, 'i64.and', '', 0)
i64_or = op(0x84, 'i64.or', '', 0)
i64_xor = op(0x85, 'i64.xor', '', 0)
i64_shl = op(0x86, 'i64.shl', '', 0)
i64_shr_s = op(0x87, 'i64.shr_s', '', 0)
i64_shr_u = op(0x88, 'i64.shr_u', '', 0)
i64_rotl = op(0x89, 'i64.rotl', '', 0)
i64_rotr = op(0x8a, 'i64.rotr', '', 0)
f32_abs = op(0x8b, 'f32.abs', '', 0)
f32_neg = op(0x8c, 'f32.neg', '', 0)
f32_ceil = op(0x8d, 'f32.ceil', '', 0)
f32_floor = op(0x8e, 'f32.floor', '', 0)
f32_trunc = op(0x8f, 'f32.trunc', '', 0)
f32_nearest = op(0x90, 'f32.nearest', '', 0)
f32_sqrt = op(0x91, 'f32.sqrt', '', 0)
f32_add = op(0x92, 'f32.add', '', 0)
f32_sub = op(0x93, 'f32.sub', '', 0)
f32_mul = op(0x94, 'f32.mul', '', 0)
f32_div = op(0x95, 'f32.div', '', 0)
f32_min = op(0x96, 'f32.min', '', 0)
f32_max = op(0x97, 'f32.max', '', 0)
f32_copysign = op(0x98, 'f32.copysign', '', 0)
f64_abs = op(0x99, 'f64.abs', '', 0)
f64_neg = op(0x9a, 'f64.neg', '', 0)
f64_ceil = op(0x9b, 'f64.ceil', '', 0)
f64_floor = op(0x9c, 'f64.floor', '', 0)
f64_trunc = op(0x9d, 'f64.trunc', '', 0)
f64_nearest = op(0x9e, 'f64.nearest', '', 0)
f64_sqrt = op(0x9f, 'f64.sqrt', '', 0)
f64_add = op(0xa0, 'f64.add', '', 0)
f64_sub = op(0xa1, 'f64.sub', '', 0)
f64_mul = op(0xa2, 'f64.mul', '', 0)
f64_div = op(0xa3, 'f64.div', '', 0)
f64_min = op(0xa4, 'f64.min', '', 0)
f64_max = op(0xa5, 'f64.max', '', 0)
f64_copysign = op(0xa6, 'f64.copysign', '', 0)
i32_wrap_i64 = op(0xa7, 'i32.wrap_i64', '', 0)
i32_trunc_sf32 = op(0xa8, 'i32.trunc_f32_s', '', 0)
i32_trunc_uf32 = op(0xa9, 'i32.trunc_f32_u', '', 0)
i32_trunc_sf64 = op(0xaa, 'i32.trunc_f64_s', '', 0)
i32_trunc_uf64 = op(0xab, 'i32.trunc_f64_u', '', 0)
i64_extend_si32 = op(0xac, 'i64.extend_i32_s', '', 0)
i64_extend_ui32 = op(0xad, 'i64.extend_i32_u', '', 0)
i64_trunc_sf32 = op(0xae, 'i64.trunc_f32_s', '', 0)
i64_trunc_uf32 = op(0xaf, 'i64.trunc_f32_u', '', 0)
i64_trunc_sf64 = op(0xb0, 'i64.trunc_f64_s', '', 0)
i64_trunc_uf64 = op(0xb1, 'i64.trunc_f64_u', '', 0)
f32_convert_si32 = op(0xb2, 'f32.convert_i32_s', '', 0)
f32_convert_ui32 = op(0xb3, 'f32.convert_i32_u', '', 0)
f32_convert_si64 = op(0xb4, 'f32.convert_i64_s', '', 0)
f32_convert_ui64 = op(0xb5, 'f32.convert_i64_u', '', 0)
f32_demote_f64 = op(0xb6, 'f32.demote_f64', '', 0)
f64_convert_si32 = op(0xb7, 'f64.convert_i32_s', '', 0)
f64_convert_ui32 = op(0xb8, 'f64.convert_i32_u', '', 0)
f64_convert_si64 = op(0xb9, 'f64.convert_i64_s', '', 0)
f64_convert_ui64 = op(0xba, 'f64.convert_i64_u', '', 0)
f64_promote_f32 = op(0xbb, 'f64.promote_f32', '', 0)
i32_reinterpret_f32 = op(0xbc, 'i32.reinterpret_f32', '', 0)
i64_reinterpret_f64 = op(0xbd, 'i64.reinterpret_f64', '', 0)
f32_reinterpret_i32 = op(0xbe, 'f32.reinterpret_i32', '', 0)
f64_reinterpret_i64 = op(0xbf, 'f64.reinterpret_i64', '', 0)

custom_section = 0x00
type_section = 0x01
import_section = 0x02
function_section = 0x03
table_section = 0x04
memory_section = 0x05
global_section = 0x06
export_section = 0x07
start_section = 0x08
element_section = 0x09
code_section = 0x0a
data_section = 0x0b

section = {
    custom_section: ['Custom'],
    type_section: ['Type'],
    import_section: ['Import'],
    function_section: ['Function'],
    table_section: ['Table'],
    memory_section: ['Memory'],
    global_section: ['Global'],
    export_section: ['Export'],
    start_section: ['Start'],
    element_section: ['Element'],
    code_section: ['Code'],
    data_section: ['Data'],
}

extern_func = 0x00
extern_table = 0x01
extern_mem = 0x02
extern_global = 0x03

extern_type = {
    extern_func: ['func'],
    extern_table: ['table'],
    extern_mem: ['mem'],
    extern_global: ['global'],
}
