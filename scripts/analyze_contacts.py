#!/usr/bin/env python3
"""Extract geometrical protein–DNA atom contacts; NOT a hydrogen-bond assignment."""
import argparse
import csv
import sys
from pathlib import Path
from Bio.PDB import NeighborSearch, is_aa
from inspect_structure import DNA_NAMES, get_structure

PHOSPHATE = {"P", "OP1", "OP2", "OP3", "O1P", "O2P", "O3P"}

def atom_is_heavy(atom):
    return str(atom.element).upper() not in {"H", "D"}

def dna_site(atom):
    name = atom.name.strip()
    if name in PHOSPHATE:
        return "phosphate"
    if "'" in name or "*" in name:
        return "sugar"
    return "base"

def extract_contacts(structure, protein_chains, dna_chains, cutoff):
    model = next(structure.get_models())
    available = set(c.id for c in model)
    required = set(protein_chains + dna_chains)
    missing = required - available
    if missing:
        raise ValueError(f"Missing chains: {sorted(missing)}; present: {sorted(available)}")
    if set(protein_chains) & set(dna_chains):
        raise ValueError("Protein and DNA chain sets must not overlap")
    p_atoms = [a for ch in protein_chains for r in model[ch] if is_aa(r, standard=True) for a in r if atom_is_heavy(a)]
    d_atoms = [a for ch in dna_chains for r in model[ch] if r.get_resname().strip() in DNA_NAMES for a in r if atom_is_heavy(a)]
    if not p_atoms or not d_atoms:
        raise ValueError("No standard amino acid or DNA heavy atoms found on specified chains")
    search = NeighborSearch(p_atoms)
    rows = []
    for d_atom in d_atoms:
        dr = d_atom.get_parent()
        dc = dr.get_parent().id
        for p_atom in search.search(d_atom.coord, cutoff, level="A"):
            pr = p_atom.get_parent()
            pc = pr.get_parent().id
            dist = p_atom - d_atom
            is_polar = str(p_atom.element).upper() in {"N", "O"} and str(d_atom.element).upper() in {"N", "O"}
            status = "potential_clash_recheck" if dist < 2.2 else "short_contact_review" if dist < 2.5 else "proximity_only"
            rows.append({
                "protein_chain":pc, "protein_residue":pr.get_resname().strip(), "protein_number":pr.id[1],
                "protein_atom":p_atom.name, "dna_chain":dc, "dna_residue":dr.get_resname().strip(),
                "dna_number":dr.id[1], "dna_atom":d_atom.name, "dna_region":dna_site(d_atom),
                "distance_A":f"{dist:.3f}", "NO_polar_atom_pair":str(is_polar).lower(), "quality_flag":status
            })
    rows.sort(key=lambda r:(r["protein_chain"],r["protein_number"],r["dna_chain"],r["dna_number"],float(r["distance_A"])))
    return rows

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("structure", help="Predicted model .pdb/.cif, NOT the original 3KMD when evaluating id143")
    ap.add_argument("--protein", default="A,D", help="Comma-separated protein chain IDs")
    ap.add_argument("--dna", default="B,C", help="Comma-separated DNA chain IDs")
    ap.add_argument("--cutoff", type=float, default=3.6, help="Heavy-atom distance cutoff in Å")
    ap.add_argument("--output", required=True, help="Output TSV")
    args=ap.parse_args()
    if args.cutoff<=0 or args.cutoff>10:
        ap.error("cutoff should be >0 and <=10 Å")
    stru=get_structure(args.structure)
    rows=extract_contacts(stru,[x.strip() for x in args.protein.split(',')],[x.strip() for x in args.dna.split(',')],args.cutoff)
    out=Path(args.output)
    out.parent.mkdir(parents=True,exist_ok=True)
    fields=["protein_chain","protein_residue","protein_number","protein_atom","dna_chain","dna_residue","dna_number","dna_atom","dna_region","distance_A","NO_polar_atom_pair","quality_flag"]
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t')
        w.writeheader()
        w.writerows(rows)
    clashes=sum(r["quality_flag"]=="potential_clash_recheck" for r in rows)
    print(f"Saved {len(rows)} atom proximity contacts to {out}; {clashes} distances < 2.2 Å flagged")
    print('Do not equate proximity or N/O proximity with a hydrogen bond; assess chemistry and angles.')

if __name__=='__main__':
    main()
