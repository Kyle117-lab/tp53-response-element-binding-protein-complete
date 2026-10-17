#!/usr/bin/env python3
"""List chains and polymer residue counts for a PDB or mmCIF structure."""
import argparse
from pathlib import Path
from Bio.PDB import PDBParser, MMCIFParser, is_aa

DNA_NAMES = {"DA", "DC", "DG", "DT", "DI", "A", "C", "G", "T", "U", "DU"}

def get_structure(path):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    if path.suffix.lower() in (".cif", ".mmcif"):
        return MMCIFParser(QUIET=True).get_structure(path.stem, str(path))
    if path.suffix.lower() in (".pdb", ".ent"):
        return PDBParser(QUIET=True).get_structure(path.stem, str(path))
    raise ValueError("Expected a .pdb or .cif/.mmcif (decompress .gz first)")

def chain_counts(structure):
    model = next(structure.get_models())
    result = []
    for ch in model:
        residues = list(ch)
        proteins = [r for r in residues if is_aa(r, standard=True)]
        dna = [r for r in residues if r.get_resname().strip() in DNA_NAMES]
        heavy_atoms = sum(1 for r in residues for a in r if str(a.element).upper() not in ("H", "D"))
        result.append((ch.id, len(proteins), len(dna), heavy_atoms))
    return result

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("structure")
    a = p.parse_args()
    structure = get_structure(a.structure)
    print("Chain\tAA residues\tDNA/RNA residues\tHeavy atoms")
    for row in chain_counts(structure):
        print("\t".join(str(v) for v in row))
    print("CHECK: template 3KMD uses protein A-D and DNA E/F; modeled complex usually uses proteins A/D and DNA B/C.")

if __name__ == "__main__":
    main()
