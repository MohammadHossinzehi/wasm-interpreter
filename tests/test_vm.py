"""Unit tests for WebAssembly VM."""

import unittest
from wasm_interpreter.vm import VM
from wasm_interpreter.memory import Memory
from wasm_interpreter.parser import Parser

class TestMemory(unittest.TestCase):
    def test_i32_load_store(self):
        mem = Memory(1)
        mem.store_i32(0, 42)
        self.assertEqual(mem.load_i32(0), 42)
    
    def test_bounds_check(self):
        mem = Memory(1)
        with self.assertRaises(RuntimeError):
            mem.load_i32(65536)
    
    def test_grow(self):
        mem = Memory(1)
        old = mem.grow(1)
        self.assertEqual(old, 1)
        self.assertEqual(mem.current_pages, 2)

class TestVM(unittest.TestCase):
    def setUp(self):
        self.vm = VM({})
    
    def test_i32_add(self):
        # Simulate: i32.const 5, i32.const 3, i32.add
        code = bytearray([0x41, 0x05, 0x41, 0x03, 0x6A, 0x0B])
        self.vm.execute(code)
        self.assertEqual(self.vm.stack[0], 8)
    
    def test_i32_sub(self):
        code = bytearray([0x41, 0x0A, 0x41, 0x03, 0x6B, 0x0B])
        self.vm.execute(code)
        self.assertEqual(self.vm.stack[0], 7)
    
    def test_i32_mul(self):
        code = bytearray([0x41, 0x06, 0x41, 0x07, 0x6C, 0x0B])
        self.vm.execute(code)
        self.assertEqual(self.vm.stack[0], 42)

class TestParser(unittest.TestCase):
    def test_parse_magic(self):
        # Valid WASM header + version
        data = b'\x00asm\x01\x00\x00\x00'
        parser = Parser(data)
        module = parser.parse()
        self.assertEqual(module['version'], 1)

if __name__ == '__main__':
    unittest.main()
