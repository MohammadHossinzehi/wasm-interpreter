"""WebAssembly binary format parser."""

import struct

class Parser:
    """Parse WebAssembly binary modules."""
    
    def __init__(self, data):
        self.data = data
        self.pos = 0
    
    def parse(self):
        """Parse a WASM module."""
        magic = self.read_bytes(4)
        if magic != b'\x00asm':
            raise ValueError('Invalid WASM magic number')
        
        version = self.read_u32()
        if version != 1:
            raise ValueError(f'Unsupported WASM version: {version}')
        
        sections = {}
        while self.pos < len(self.data):
            section_id = self.read_u8()
            section_size = self.read_leb128_u32()
            section_data = self.read_bytes(section_size)
            sections[section_id] = section_data
        
        return {
            'version': version,
            'sections': sections,
        }
    
    def read_u8(self):
        val = self.data[self.pos]
        self.pos += 1
        return val
    
    def read_u32(self):
        val = struct.unpack('<I', self.data[self.pos:self.pos+4])[0]
        self.pos += 4
        return val
    
    def read_i32(self):
        val = struct.unpack('<i', self.data[self.pos:self.pos+4])[0]
        self.pos += 4
        return val
    
    def read_bytes(self, n):
        val = self.data[self.pos:self.pos+n]
        self.pos += n
        return val
    
    def read_leb128_u32(self):
        """Read unsigned LEB128 integer."""
        result = 0
        shift = 0
        while True:
            byte = self.read_u8()
            result |= (byte & 0x7F) << shift
            if (byte & 0x80) == 0:
                break
            shift += 7
        return result
    
    def read_leb128_i32(self):
        """Read signed LEB128 integer."""
        result = 0
        shift = 0
        byte = 0
        while True:
            byte = self.read_u8()
            result |= (byte & 0x7F) << shift
            shift += 7
            if (byte & 0x80) == 0:
                break
        if shift < 32 and (byte & 0x40):
            result |= -(1 << shift)
        return result
