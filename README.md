# wasm-interpreter

A WebAssembly bytecode interpreter written from scratch in Python. This project implements core WASM instructions, linear memory management, and function call semantics without external dependencies.

## What It Does

This interpreter can:
- Parse WebAssembly binary format (module structure, type definitions, imports/exports)
- Execute core instruction set: arithmetic (i32.add, i32.sub, etc.), logical ops, memory operations, and control flow
- Maintain linear memory with proper bounds checking
- Support function calls with local variables and parameter passing
- Execute nested blocks and branches (if/else, block, loop)
- Provide execution tracing for debugging

## Why This Exists

WebAssembly is everywhere, but most developers have never seen the bytecode or understood how it actually executes. This project demystifies WASM by implementing a real interpreter from scratch—no libwasmvm, no external toolchain, just pure Python. Useful for learning, debugging, and embedded WASM execution.

## Installation

Clone and install (no external dependencies):

```bash
pip install -e .
```

## Quick Start

```python
from wasm_interpreter.vm import VM
from wasm_interpreter.parser import Parser

# Load a WASM binary file
with open('example.wasm', 'rb') as f:
    binary = f.read()

# Parse and execute
parser = Parser(binary)
module = parser.parse()
vm = VM(module)

# Call exported function
result = vm.call('add', [5, 3])
print(result)  # Output: [8]
```

## Architecture

- **parser.py**: Reads WebAssembly binary format, validates structure
- **instructions.py**: Core opcode definitions and handlers (i32, i64, f32, f64, memory, control flow)
- **vm.py**: Main execution engine with stack-based computation
- **memory.py**: Linear memory implementation with bounds checking
- **test_*.py**: Comprehensive unit tests for each component

## Features

- Full i32 and i64 arithmetic/logic support
- Memory operations (load, store) with proper alignment
- Function calls with local variable scoping
- Block/loop/branch control flow
- Call stack tracing for debugging
- Comprehensive error reporting

## Testing

```bash
python -m pytest tests/
```

The test suite covers parsing, instruction execution, memory operations, and edge cases.

## Design Notes

- Stack-based VM: follows WebAssembly's design exactly
- No JIT: interpreted bytecode for clarity and inspection
- Pure Python: teaches implementation details without C/Rust overhead
- Modular: each file handles one concern (parsing, execution, memory)

## Limitations

This is an educational interpreter, not production-grade:
- No floating-point instructions (f32/f64)
- No SIMD or bulk operations
- No tail calls or reference types
- Limited to single-threaded execution

For production WASM execution, use wasmtime or similar.

## License

MIT
