"""WebAssembly virtual machine."""

from .memory import Memory
from .instructions import HANDLERS

class VM:
    """Stack-based WebAssembly execution engine."""
    
    def __init__(self, module, memory_pages=1):
        self.module = module
        self.memory = Memory(memory_pages)
        self.stack = []
        self.locals = []
        self.globals = {}
        self.functions = {}
        self.call_stack = []
        self.pc = 0
        self.halted = False
    
    def call(self, func_name, args):
        """Call an exported function by name."""
        if func_name not in self.functions:
            raise ValueError(f'Function not found: {func_name}')
        
        func = self.functions[func_name]
        self.stack = list(args)
        self.execute(func['code'])
        return self.stack if self.stack else [0]
    
    def execute(self, code):
        """Execute bytecode."""
        self.pc = 0
        while self.pc < len(code) and not self.halted:
            opcode = code[self.pc]
            self.pc += 1
            
            if opcode == 0x00:  # unreachable
                raise RuntimeError('Unreachable instruction executed')
            elif opcode == 0x01:  # nop
                pass
            elif opcode == 0x0B:  # end
                self.halted = True
            elif opcode == 0x41:  # i32.const
                val = self.read_leb128_i32(code)
                self.stack.append(val)
            elif opcode == 0x42:  # i64.const
                val = self.read_leb128_i64(code)
                self.stack.append(val)
            elif opcode == 0x6A:  # i32.add
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append((a + b) & 0xFFFFFFFF)
            elif opcode == 0x6B:  # i32.sub
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append((a - b) & 0xFFFFFFFF)
            elif opcode == 0x6C:  # i32.mul
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append((a * b) & 0xFFFFFFFF)
            elif opcode == 0x71:  # i32.and
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a & b)
            elif opcode == 0x72:  # i32.or
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a | b)
            elif opcode == 0x73:  # i32.xor
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a ^ b)
            else:
                raise RuntimeError(f'Unknown opcode: 0x{opcode:02X}')
    
    def read_leb128_i32(self, code):
        """Read signed LEB128."""
        result = 0
        shift = 0
        byte = 0
        while True:
            byte = code[self.pc]
            self.pc += 1
            result |= (byte & 0x7F) << shift
            shift += 7
            if (byte & 0x80) == 0:
                break
        if shift < 32 and (byte & 0x40):
            result |= -(1 << shift)
        return result
    
    def read_leb128_i64(self, code):
        """Read signed LEB128 as 64-bit."""
        result = 0
        shift = 0
        byte = 0
        while True:
            byte = code[self.pc]
            self.pc += 1
            result |= (byte & 0x7F) << shift
            shift += 7
            if (byte & 0x80) == 0:
                break
        if shift < 64 and (byte & 0x40):
            result |= -(1 << shift)
        return result
