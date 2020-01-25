#!/bin/sh

python3 obfuscator.py example2.py
uncompyle6 example2.obf.pyc > example2.decompile.py

echo "Original bytecode:"
python3 example2.obf.pyc

echo "Decompiled code"
python3 example2.decompile.py
