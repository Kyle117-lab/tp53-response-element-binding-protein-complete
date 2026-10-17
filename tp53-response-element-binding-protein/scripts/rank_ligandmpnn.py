#!/usr/bin/env python3
"""Rank LigandMPNN FASTA records by their recorded ligand_confidence."""
import argparse
import csv
import re
from pathlib import Path

def read_records(path):
    head=None; seq=[]
    for raw in Path(path).read_text().splitlines():
        line=raw.strip()
        if not line: continue
        if line.startswith('>'):
            if head is not None: yield head,''.join(seq)
            head=line[1:];seq=[]
        else: seq.append(line)
    if head is not None: yield head,''.join(seq)

def get_field(h,field):
    m=re.search(r'\b'+re.escape(field)+r'=([\d.eE+\-]+)',h)
    return float(m.group(1)) if m else None

def rank(path):
    results=[]
    for header,sequence in read_records(path):
        m=re.search(r'\bid=(\d+)\b',header)
        if not m: continue
        results.append({'id':int(m.group(1)),'ligand_confidence':get_field(header,'ligand_confidence'), 'overall_confidence':get_field(header,'overall_confidence'),'sequence_length':len(sequence),'sequence':sequence})
    results.sort(key=lambda a: a['ligand_confidence'] if a['ligand_confidence'] is not None else -1.0,reverse=True)
    return results

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('fasta')
    ap.add_argument('--output', default='results/ligandmpnn_ranked.tsv')
    ap.add_argument('--top',type=int,default=10)
    a=ap.parse_args()
    data=rank(a.fasta)
    if not data: ap.error('No LigandMPNN design IDs found; check FASTA header format')
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0]),delimiter='\t');w.writeheader();w.writerows(data)
    print(f'Wrote {len(data)} designs to {out}. Top IDs:',[x['id'] for x in data[:a.top]])

if __name__=='__main__': main()
