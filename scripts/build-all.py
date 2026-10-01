#!/usr/bin/env python3
"""Render dua proyek Quarto dan HTML mandiri, dengan aset SVG yang disertakan."""
from pathlib import Path
import argparse
import shutil
import subprocess
import sys

p=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--quarto',default='quarto',help='Nama atau path executable Quarto')
args=parser.parse_args()
subprocess.run([sys.executable,str(p/'scripts/build-reading.py')],check=True,cwd=p)
for source in ['book','slides','reading/buku.qmd']:
 subprocess.run([args.quarto,'render',source],check=True,cwd=p)
shutil.copy2(p/'slides/_slides/kuliah.html',p/'reading/kuliah.html')
print('Selesai: book/_book/index.html, reading/buku.html, reading/kuliah.html')
