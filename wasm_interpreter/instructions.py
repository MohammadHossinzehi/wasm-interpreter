"""WebAssembly instruction definitions and handlers."""

# Opcode definitions
OPCODES = {
    0x20: 'local.get',      0x21: 'local.set',
    0x22: 'local.tee',      0x23: 'global.get',
    0x24: 'global.set',     0x28: 'i32.load',
    0x29: 'i64.load',       0x2A: 'f32.load',
    0x2B: 'f64.load',       0x2C: 'i32.load8_s',
    0x2D: 'i32.load8_u',    0x2E: 'i32.load16_s',
    0x2F: 'i32.load16_u',   0x36: 'i32.store',
    0x37: 'i64.store',      0x38: 'f32.store',
    0x39: 'f64.store',      0x3A: 'i32.store8',
    0x3B: 'i32.store16',    0x3F: 'memory.size',
    0x40: 'memory.grow',    0x41: 'i32.const',
    0x42: 'i64.const',      0x43: 'f32.const',
    0x44: 'f64.const',      0x45: 'i32.eqz',
    0x46: 'i32.eq',         0x47: 'i32.ne',
    0x48: 'i32.lt_s',       0x49: 'i32.lt_u',
    0x4A: 'i32.gt_s',       0x4B: 'i32.gt_u',
    0x4C: 'i32.le_s',       0x4D: 'i32.le_u',
    0x4E: 'i32.ge_s',       0x4F: 'i32.ge_u',
    0x50: 'i64.eqz',        0x51: 'i64.eq',
    0x6A: 'i32.add',        0x6B: 'i32.sub',
    0x6C: 'i32.mul',        0x6D: 'i32.div_s',
    0x6E: 'i32.div_u',      0x6F: 'i32.rem_s',
    0x70: 'i32.rem_u',      0x71: 'i32.and',
    0x72: 'i32.or',         0x73: 'i32.xor',
    0x74: 'i32.shl',        0x75: 'i32.shr_s',
    0x76: 'i32.shr_u',      0x77: 'i32.rotl',
    0x78: 'i32.rotr',       0x7C: 'i64.add',
    0x0B: 'end',            0x05: 'else',
    0x0C: 'br',             0x0D: 'br_if',
    0x0E: 'br_table',       0x00: 'unreachable',
    0x01: 'nop',            0x02: 'block',
    0x03: 'loop',           0x04: 'if',
    0x10: 'call',           0x11: 'call_indirect',
}

def execute_i32_add(stack, memory=None):
    b = stack.pop()
    a = stack.pop()
    stack.append((a + b) & 0xFFFFFFFF)

def execute_i32_sub(stack, memory=None):
    b = stack.pop()
    a = stack.pop()
    stack.append((a - b) & 0xFFFFFFFF)

def execute_i32_mul(stack, memory=None):
    b = stack.pop()
    a = stack.pop()
    stack.append((a * b) & 0xFFFFFFFF)

def execute_i32_and(stack, memory=None):
    b = stack.pop()
    a = stack.pop()
    stack.append(a & b)

def execute_i32_or(stack, memory=None):
    b = stack.pop()
    a = stack.pop()
    stack.append(a | b)

def execute_i32_xor(stack, memory=None):
    b = stack.pop()
    a = stack.pop()
    stack.append(a ^ b)

def execute_i32_load(stack, memory, offset):
    addr = stack.pop() + offset
    stack.append(memory.load_i32(addr))

def execute_i32_store(stack, memory, offset):
    addr = stack.pop() + offset
    val = stack.pop()
    memory.store_i32(addr, val)

def execute_i32_const(stack, value):
    stack.append(value & 0xFFFFFFFF)

def execute_i32_eq(stack, memory=None):
    b = stack.pop()
    a = stack.pop()
    stack.append(1 if a == b else 0)

def execute_i32_lt_s(stack, memory=None):
    b = stack.pop()
    a = stack.pop()
    stack.append(1 if a < b else 0)

HANDLERS = {
    'i32.add': execute_i32_add,
    'i32.sub': execute_i32_sub,
    'i32.mul': execute_i32_mul,
    'i32.and': execute_i32_and,
    'i32.or': execute_i32_or,
    'i32.xor': execute_i32_xor,
    'i32.load': execute_i32_load,
    'i32.store': execute_i32_store,
    'i32.const': execute_i32_const,
    'i32.eq': execute_i32_eq,
    'i32.lt_s': execute_i32_lt_s,
}
