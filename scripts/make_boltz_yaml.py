#!/usr/bin/env python3
"""Create a valid two-protein/two-DNA Boltz YAML from a real LigandMPNN FASTA design ID."""
import argparse
import re
from pathlib import Path
import yaml
from rank_ligandmpnn import read_records

DNA="GGGCATGCCTAGGCATGCCC"
AA=set('ACDEFGHIKLMNPQRSTVWY')

def get_design(fasta,id_num):
    hits=[]
    for header,sequence in read_records(fasta):
        m=re.search(r'\bid=(\d+)\b',header)
        if m and int(m.group(1))==id_num:
            hits.append((header,sequence.upper()))
    if len(hits)!=1:
        raise ValueError(f'Expected exactly one id={id_num} in {fasta}, found {len(hits)}; verify batch provenance')
    seq=hits[0][1]
    if not seq or not set(seq)<=AA:
        raise ValueError('Invalid or nonstandard protein sequence characters (A-Z; canonical amino acids only)')
    return seq

def make_yaml(seq):
    return {'version':1,'sequences':[{'protein':{'id':'A','sequence':seq}},{'protein':{'id':'D','sequence':seq}},{'dna':{'id':'B','sequence':DNA}},{'dna':{'id':'C','sequence':DNA}}]}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--fasta',required=True)
    ap.add_argument('--id',required=True,type=int)
    ap.add_argument('--out',required=True)
    a=ap.parse_args()
    seq=get_design(a.fasta,a.id)
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(yaml.safe_dump(make_yaml(seq),sort_keys=False))
    print(f'Saved {out}: protein length {len(seq)}, same chain A/D sequence, 20nt palindrome B/C')

if __name__=='__main__': main()
