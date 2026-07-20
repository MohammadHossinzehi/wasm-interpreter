"""WebAssembly linear memory implementation."""

class Memory:
    """Linear memory with bounds checking and alignment."""
    
    def __init__(self, initial_pages=1, max_pages=None):
        """Initialize memory.
        
        Args:
            initial_pages: Initial number of 64KB pages
            max_pages: Maximum number of pages (None = unlimited)
        """
        self.page_size = 65536
        self.data = bytearray(initial_pages * self.page_size)
        self.max_pages = max_pages or float('inf')
        self.current_pages = initial_pages
    
    def size(self):
        """Return memory size in bytes."""
        return len(self.data)
    
    def load_i32(self, address):
        """Load 32-bit signed integer."""
        self._check_bounds(address, 4)
        return int.from_bytes(self.data[address:address+4], 'little', signed=True)
    
    def load_i64(self, address):
        """Load 64-bit signed integer."""
        self._check_bounds(address, 8)
        return int.from_bytes(self.data[address:address+8], 'little', signed=True)
    
    def load_u8(self, address):
        """Load unsigned 8-bit value."""
        self._check_bounds(address, 1)
        return self.data[address]
    
    def store_i32(self, address, value):
        """Store 32-bit signed integer."""
        self._check_bounds(address, 4)
        self.data[address:address+4] = int(value).to_bytes(4, 'little', signed=True)
    
    def store_i64(self, address, value):
        """Store 64-bit signed integer."""
        self._check_bounds(address, 8)
        self.data[address:address+8] = int(value).to_bytes(8, 'little', signed=True)
    
    def store_u8(self, address, value):
        """Store unsigned 8-bit value."""
        self._check_bounds(address, 1)
        self.data[address] = int(value) & 0xFF
    
    def grow(self, pages):
        """Grow memory by pages. Returns old page count or -1."""
        if self.current_pages + pages > self.max_pages:
            return -1
        old_pages = self.current_pages
        new_size = (self.current_pages + pages) * self.page_size
        self.data.extend(bytearray(pages * self.page_size))
        self.current_pages += pages
        return old_pages
    
    def _check_bounds(self, address, length):
        """Check if memory access is within bounds."""
        if address < 0 or address + length > len(self.data):
            raise RuntimeError(f"Memory access out of bounds: {address}+{length} > {len(self.data)}")
