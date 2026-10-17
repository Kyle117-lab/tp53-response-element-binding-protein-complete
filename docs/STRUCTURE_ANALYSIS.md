# Structural inspection: id143 / 3KMD

## Chain map

- `results/structures/id143_design_complex.pdb`: protein A/D (123 aa each), DNA B/C (20 nt each).
- `inputs/3KMD.pdb`: TP53 proteins A–D and DNA E/F (reference template; numbering differs from id143).

## ChimeraX

1. Start ChimeraX (the desktop application).
2. Use **File → Open** to load `chimerax/id143_cartoon_DNA_stick.cxc`. This command file loads the design PDB using a relative path, so start ChimeraX in the repository root (or edit the `open` line to the absolute path).
3. To view reference 3KMD instead, open `chimerax/3KMD_reference.cxc` in a fresh session.

The visualization uses cyan/yellow protein cartoon chains and olive stick DNA, with selected residues shown as atoms and N/O colors. It does not by itself establish contact chemistry.

## CPU geometry analysis

```bash
python scripts/analyze_contacts.py results/structures/id143_design_complex.pdb --cutoff 3.6 \
   --output results/id143_atom_contacts_3p6A.tsv
```

The TSV contains heavy-atom pairs up to the chosen Euclidean cutoff. `NO_polar_atom_pair` simply means both atom elements are N or O; the script does **not** evaluate the donor/acceptor roles, protonation or H-bond angle. Distances below 2.2 Å are flagged as potentially clashing; intermediate 2.2–2.5 Å contacts need review. Check nearby base atoms vs sugar/phosphate atoms separately.

## Interface checks

- Does the DNA remain approximately duplex-like and free of severe distortion?
- Are protein side-chain atoms positioned plausibly (no clashes)?
- Are base-specific polar contacts retained across both protein monomers?
- Is the binding pose reproducible across multiple Boltz seeds?
- Do the full confidence metrics and interface confidence support the pose?

**Known issue:** the deposited PDB yields 42 protein–DNA heavy atom pairs below 2.2 Å at 3.6 Å cutoff. This is a model quality warning. See `results/id143_contact_audit.txt`. In prior poster illustrations, the printed 1.469 Å contact should not be quoted without confirming the exact atom pair; the deposited model's A:LYS115 NZ → C:DT16 OP1 is 2.320 Å.
