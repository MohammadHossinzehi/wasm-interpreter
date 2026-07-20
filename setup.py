"""Setup configuration for wasm-interpreter package."""

from setuptools import setup, find_packages

setup(
    name='wasm-interpreter',
    version='0.1.0',
    description='WebAssembly bytecode interpreter in pure Python',
    author='Mohammad Hossin Zehi',
    packages=find_packages(),
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
