#!/usr/bin/env python3
"""Menyatukan sumber buku untuk HTML mandiri; render menggunakan Quarto."""
from pathlib import Path
import shutil
P=Path(__file__).resolve().parents[1]
R=P/'reading';R.mkdir(exist_ok=True)
appendices=['glosarium.qmd','lembar-kerja.qmd','panduan-kuliah.qmd','kunci-latihan.qmd']
files=[P/'book/index.qmd']+sorted((P/'book/chapters').glob('*.qmd'))+[P/'book/appendices'/name for name in appendices]+[P/'book/references.qmd']
text=[]
for f in files:
 s=f.read_text()
 if f.parent.name=='appendices':
  letter=chr(65+appendices.index(f.name))
  title,rest=s.split('\n',1)
  s=f'# Lampiran {letter}: {title[2:]} {{.unnumbered}}\n'+rest
 if f.name=='index.qmd':s=s.replace('](assets/','](../assets/')
 s=s.replace('{{< include ../includes/simulation-results.qmd >}}',(P/'book/includes/simulation-results.qmd').read_text())
 text.append(s)
header='''---
title: "Rekayasawan Paripurna"
subtitle: "TISE, riset, dan rekayasa yang cerdas serta mencerdaskan"
author: "Armein Z. R. Langi"
date: "2026-10-01"
lang: id
bibliography: ../references.bib
format:
  html:
    theme: cosmo
    html-math-method: mathml
    css: ../assets/book.css
    toc: true
    toc-depth: 2
    number-sections: true
    embed-resources: true
    code-copy: true
    mainfont: "DejaVu Sans"
    fontsize: 1.02em
execute:
  enabled: false
---

'''
(R/'buku.qmd').write_text(header+'\n\n'.join(text))
shutil.copytree(P/'assets',P/'book/assets',dirs_exist_ok=True)
print('reading source',len(files),'sections')
