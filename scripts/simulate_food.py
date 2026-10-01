#!/usr/bin/env python3
"""Simulasi pedagogis pangan. Seluruh data sintetik, bukan hasil penelitian."""
from pathlib import Path
import csv, json, random, math
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; PLOTS=ROOT/'assets/plots'; INC=ROOT/'book/includes'
for p in [DATA,PLOTS,INC]: p.mkdir(parents=True,exist_ok=True)
rng=random.Random(1962)
rows=[]
for day in range(1,31):
    shock=170 if 11<=day<=14 else 0
    demand=max(200,round(550+70*math.sin(day*2*math.pi/7)+rng.uniform(-40,40)+shock))
    capacity=450 if day in [18,19,20] else 700
    rows.append({'hari':day,'permintaan':demand,'kapasitas':capacity})
summary={}
for name in ['Tetap','Adaptif']:
    prev=550; totals={'produksi':0,'penjualan':0,'sisa':0,'kekurangan':0,'margin_rp':0}
    for r in rows:
        q=min(r['kapasitas'],550 if name=='Tetap' else round(.7*prev+.3*550))
        sold=min(r['permintaan'],q);waste=max(q-r['permintaan'],0);unmet=max(r['permintaan']-q,0)
        margin=20000*sold-14000*q-1000*waste
        for k,v in [('produksi',q),('penjualan',sold),('sisa',waste),('kekurangan',unmet),('margin_rp',margin)]: totals[k]+=v
        r['produksi_'+name.lower()]=q
        r['sisa_'+name.lower()]=waste
        prev=r['permintaan']
    totals['cakupan_persen']=100*totals['penjualan']/sum(r['permintaan'] for r in rows)
    totals['sisa_persen']=100*totals['sisa']/totals['produksi']
    summary[name]=totals
with (DATA/'food-synthetic.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(DATA/'food-summary.json').write_text(json.dumps({'status':'data sintetik pedagogis','seed':1962,'days':30,'policies':summary},indent=2))
lines=['| Ukuran, 30 hari sintetik | Tetap | Adaptif |','|---|---:|---:|']
metrics=[('Cakupan permintaan (%)','cakupan_persen'),('Sisa/produksi (%)','sisa_persen'),('Penjualan (porsi)','penjualan'),('Sisa (porsi)','sisa'),('Kekurangan (porsi)','kekurangan'),('Margin sederhana (Rp)','margin_rp')]
for label,key in metrics:
    vals=[]
    for policy in ['Tetap','Adaptif']:
        v=summary[policy][key]
        vals.append((f'{v:.2f}' if isinstance(v,float) else f'{v:,}').replace(',','.'))
    lines.append('| '+label+' | '+' | '.join(vals)+' |')
(INC/'simulation-results.qmd').write_text('\n'.join(lines)+'\n\nSeluruh angka adalah keluaran simulasi sintetik dengan seed 1962.\n')
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':14,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#173c50','text.color':'#173c50','svg.fonttype':'none'})
    fig,ax=plt.subplots(figsize=(12,5.5))
    x=[r['hari'] for r in rows]
    for key,label,color,ls in [('permintaan','Permintaan','#173c50','-'),('kapasitas','Kapasitas','#a6652d','--'),('produksi_tetap','Produksi tetap','#7e969f',':'),('produksi_adaptif','Produksi adaptif','#007f85','-')]:
        ax.plot(x,[r[key] for r in rows],label=label,color=color,linestyle=ls,lw=2.5)
    ax.set(xlabel='Hari sintetik',ylabel='Porsi per hari',ylim=(0,900),xlim=(1,30))
    ax.grid(axis='y',alpha=.2);ax.legend(loc='lower left',ncol=2,frameon=False)
    fig.suptitle('Produksi pada permintaan dan kapasitas yang berubah',fontsize=18,fontweight='bold')
    fig.text(.08,.01,'Ilustrasi sintetik. Bukan data lapangan.',fontsize=12)
    fig.tight_layout(rect=(0,.04,1,.93));fig.savefig(PLOTS/'food-timeseries.svg');plt.close(fig)
    fig,axs=plt.subplots(1,2,figsize=(12,5.5))
    for ax,key,title in zip(axs,['cakupan_persen','sisa_persen'],['Cakupan: penjualan / permintaan (%)','Sisa / produksi (%)']):
        v=[summary[k][key] for k in ['Tetap','Adaptif']]
        bars=ax.bar(['Tetap','Adaptif'],v,color=['#7e969f','#007f85'],width=.55)
        ax.set_title(title,fontsize=15,pad=15);ax.set_ylim(0,100 if key=='cakupan_persen' else max(v)*1.5)
        ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
        ax.bar_label(bars,labels=[f'{x:.2f}%' for x in v],padding=7,fontsize=16)
    fig.text(.08,.01,'Ilustrasi sintetik, 30 hari. Penyebut mengikuti label tiap panel.',fontsize=12)
    fig.tight_layout(rect=(0,.05,1,1));fig.savefig(PLOTS/'food-outcomes.svg');plt.close(fig)
    x=list(range(0,13));grow=[40+4*i for i in x];flat=[40+.5*i for i in x]
    fig,ax=plt.subplots(figsize=(12,5.5))
    ax.plot(x,grow,label='Hipotesis desain yang mencerdaskan',color='#007f85',lw=3,marker='o')
    ax.plot(x,flat,label='Skenario kapabilitas relatif tetap',color='#a6652d',lw=3,ls='--')
    ax.set(xlabel='Sesi penggunaan ilustratif',ylabel='Skor kapabilitas arbitrer',ylim=(0,100),xlim=(0,12))
    ax.grid(axis='y',alpha=.2);ax.legend(frameon=False,loc='upper left')
    fig.suptitle('Kapabilitas manusia sebagai outcome sepanjang waktu',fontsize=18,fontweight='bold')
    fig.text(.08,.01,'Kurva konseptual sintetik. Skala arbitrer, bukan instrumen atau bukti empiris.',fontsize=12)
    fig.tight_layout(rect=(0,.04,1,.93));fig.savefig(PLOTS/'capability.svg');plt.close(fig)
except ImportError:
    print('CSV dan tabel dibuat. Install matplotlib untuk meregenerasi plot.')
print(json.dumps(summary,indent=2))
