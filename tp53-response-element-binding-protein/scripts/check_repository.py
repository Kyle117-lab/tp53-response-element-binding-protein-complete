#!/usr/bin/env python3
"""Validate shipped core artifacts and warn about absent historical intermediates."""
import hashlib,json,sys
from pathlib import Path
from Bio.PDB import PDBParser, is_aa
from Bio.SeqUtils import seq1
import yaml
ROOT=Path(__file__).resolve().parent.parent
DNA={'DA':'A','DT':'T','DG':'G','DC':'C'}

def check():
    path=ROOT/'results/structures/id143_design_complex.pdb'
    assert path.is_file(),f'Missing real id143 structure: {path}'
    model=PDBParser(QUIET=True).get_structure('id143',str(path))[0]
    assert set(c.id for c in model)=={'A','D','B','C'}, 'Unexpected id143 chain IDs'
    seqs={ch:''.join(seq1(r.resname) for r in model[ch] if is_aa(r, standard=True)) for ch in ('A','D')}
    dnas={ch:''.join(DNA[r.resname] for r in model[ch]) for ch in ('B','C')}
    assert seqs['A']==seqs['D'] and len(seqs['A'])==123
    assert dnas['B']==dnas['C']=='GGGCATGCCTAGGCATGCCC'
    y=yaml.safe_load((ROOT/'boltz_input/id143_homodimer.yaml').read_text())
    assert y['version']==1
    for el in y['sequences']:
        info=el.get('protein') or el.get('dna')
        ch=info['id']
        assert info['sequence']==(seqs[ch] if ch in seqs else dnas[ch]), f'YAML sequence mismatch: {ch}'
    fasta=(ROOT/'sequences/id143_protein.fasta').read_text()
    assert seqs['A'] in fasta
    cfg=json.loads((ROOT/'inputs/rfd3_na_test9.json').read_text())
    spec=next(iter(cfg.values()))
    assert spec['input']=='inputs/3KMD.pdb'
    assert (ROOT/'inputs/3KMD.pdb').is_file()
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    print('PASS: actual id143 model chains, sequence, Boltz input, RFD3 reference configuration')
    print('id143 SHA256:',digest)
    print('WARNING: original historical Boltz JSON, RFD3 selected CIF and LigandMPNN batch FASTA are not provided')
    return True
if __name__=='__main__':
    sys.exit(0 if check() else 1)
