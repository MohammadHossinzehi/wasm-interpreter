"""WebAssembly interpreter package."""

__version__ = "0.1.0"

from .vm import VM
from .parser import Parser

__all__ = ["VM", "Parser", "__version__"]
