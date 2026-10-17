# TP53 Response Element–Binding Protein: AI-Assisted De Novo Design

[![Check repository](../../actions/workflows/validate.yml/badge.svg)](../../actions/workflows/validate.yml)

**Project:** Computational design of a candidate DNA-binding protein inspired by the TP53–DNA complex (PDB **3KMD**).  
**Workflow:** **RFD3 / RFdiffusion-NA → LigandMPNN → Boltz → UCSF ChimeraX**  
**Representative design:** **id143** (**included as an actual structural PDB and sequence**, submitted as `143(1).pdb`).  
**Research status:** **In silico prediction only**; DNA-binding affinity, sequence specificity, and TP53-equivalent biological function **have not been experimentally demonstrated**.

## Quick start: explore the real id143 result (CPU only)

```bash
git clone https://github.com/<YOUR-USERNAME>/tp53-response-element-binding-protein.git
cd tp53-response-element-binding-protein
python3 -m pip install -r requirements-analysis.txt
python3 scripts/check_repository.py
python3 scripts/inspect_structure.py results/structures/id143_design_complex.pdb
python3 scripts/analyze_contacts.py results/structures/id143_design_complex.pdb \
  --protein A,D --dna B,C --cutoff 3.6 --output results/id143_contacts_recomputed.tsv
```

Or **download the ZIP**, unzip, and run the commands after `cd tp53-response-element-binding-protein`—no Git account is needed for local inspection. To view the model interactively, open the PDB in [UCSF ChimeraX](https://www.rbvi.ucsf.edu/chimerax/), then open `chimerax/id143_cartoon_DNA_stick.cxc` in the ChimeraX command interface (the script loads the model itself).

## What is actually included?

| File or folder | Purpose / provenance |
|---|---|
| `results/structures/id143_design_complex.pdb` | **User-supplied final representative PDB**: two protein chains A/D and two DNA chains B/C. |
| `sequences/id143_protein.fasta` | Extracted **directly from chain A** (123 amino acids); identical chain D. |
| `sequences/id143_dna.fasta` | Extracted from the submitted PDB (20 nt per strand). |
| `boltz_input/id143_homodimer.yaml` | Prediction input reconstructed from the **actual PDB sequences**; not claimed as the original historical YAML. |
| `results/id143_atom_contacts_3p6A.tsv` | **Recomputed** heavy-atom proximity contacts from the submitted PDB (3.6 Å cutoff). Not validated hydrogen bonds. |
| `results/id143_contact_audit.txt` | Geometry review including serious short-distance warnings. |
| `results/id143_reported_boltz_metrics.tsv` | Scores supplied in earlier study notes; **not derived from the PDB** (requires original Boltz JSON). |
| `results/id143_reported_hbond_log_contacts.tsv` | Earlier H-bond log values, cross-checked against new PDB in `results/id143_reference_contacts_verified.tsv`. |
| `inputs/3KMD.pdb` | **Original PDB 3KMD reference structure**, separate from the designed id143. |
| `inputs/rfd3_na_test9.json` | Reconstructed/documented t9 full-DNA, motif-conditioned backbone design configuration. |
| `scripts/` | Reusable shell commands and analysis utilities. |
| `figures/` | Prior presentation figures and poster; these are **illustrations**, not independent experimental evidence. |

**Why both 3KMD and id143?** The earlier user attachment named `143.pdb` was in fact the **original 3KMD reference** (its chains and coordinates identify a TP53–DNA structure); the newer attachment `143(1).pdb` contains the **actual designed id143 complex**, saved unmodified in `results/structures/id143_design_complex.pdb`. Do not interchange them.

### Selected model structural summary (directly derived from supplied PDB)

| Chain | Component | Length | Sequence |
|---|---|---:|---|
| A | Designed protein | 123 aa | `sequences/id143_protein.fasta` |
| D | Designed protein | 123 aa | Identical to chain A |
| B | DNA | 20 nt | `GGGCATGCCTAGGCATGCCC` |
| C | DNA | 20 nt | `GGGCATGCCTAGGCATGCCC` |

The DNA strand sequences are palindromic in 5′→3′ form and identical; verify molecular strand direction during any alternative format conversion.

## Experimental design: historical pipeline

1. **Reference:** use 3KMD, TP53 proteins on chains A–D and DNA on chains E/F (check chain numbering in your own download).
2. **RFD3:** condition on TP53 chain A motifs **118–124, 241–248 and 273–285**, constrain the DNA, and generate candidate protein backbones. The documented t9 configuration requested **4 × 25 = 100 samples**, *not necessarily 100 successfully produced structures*.
3. **LigandMPNN:** design amino acid sequences with DNA context for a selected RFD3 backbone (in that RFD3 output protein usually appeared on chain **C**).
4. **Boltz:** predict protein homodimer + double-stranded DNA structures. A later 20-nt DNA model was used for Boltz; it differs from the original 3KMD t9 19-nt input.
5. **Evaluate:** rank using complex confidence metrics **and** DNA geometry, atom clashes, and residue–DNA interaction chemistry. The final representative model is called **id143**.
6. **Inspect:** ChimeraX cartoon protein, stick DNA, residue–base contacts, distance measurements.

**Critical reproducibility distinction:** We provide the **final id143 sequence/structure**, but **not** the original full intermediate RFD3/LigandMPNN outputs, random seeds, conda environment lockfiles, checkpoint weights, original id143 Boltz confidence JSON, or training code. Therefore, the full historical path to obtain *exactly id143* from scratch is **not guaranteed reproducible** using this repository alone. The CPU-only geometric analysis **is** reproducible.

## Run computational pipeline (optional GPU required)

See [`docs/INSTALLATION.md`](docs/INSTALLATION.md) and [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md) first.

```bash
# A. RFD3: requires NVIDIA GPU, Docker/Foundry image, compatible checkpoint
bash scripts/run_rfd3.sh

# B. LigandMPNN: choose a real RFD3 CIF file first; default filename is t9 example
conda activate pmpnn
bash scripts/run_ligandmpnn.sh /absolute/path/to/selected_rfd3_backbone.cif

# C. Boltz: the included YAML uses the actual submitted id143 sequence
conda activate boltz
bash scripts/run_boltz.sh boltz_input/id143_homodimer.yaml
```

Boltz results may vary with program version, seeds, MSA, and preprocessing. The shipped `results/structures/id143_design_complex.pdb` is **a real submitted artifact**, not the guaranteed result of rerunning these commands.

## Model scores from earlier research notes

| Candidate | Confidence | ipTM | pTM | Complex pLDDT |
|---|---:|---:|---:|---:|
| id143 | 0.7214 | 0.8977 | 0.9003 | 0.6773 |

These figures were reported in the research record; **the PDB contains no Boltz scoring JSON**, so they are not independently computable from this file. See `results/id143_reported_boltz_metrics.tsv`.

## Interface verification and cautions

The actual PDB confirms representative geometry (Å; heavy-atom distances, **not proof of hydrogen bonds**):

| Protein atom | DNA atom | Distance (Å) | Interpretation |
|---|---|---:|---|
| A:ARG103 NH1 | B:DG3 O6 | 3.037 | Guanine O6 proximity |
| D:ARG103 NH1 | C:DG3 O6 | 3.337 | Guanine O6 proximity |
| A:ARG88 NH2 | C:DG13 O6 | 3.380 | Guanine O6 proximity |
| D:ARG88 NH2 | B:DG13 O6 | 3.275 | Guanine O6 proximity |
| A:SER106 OG | C:DT16 O4 | 3.074 | Thymine O4 proximity |
| D:SER106 OG | B:DT16 O4 | 2.893 | Thymine O4 proximity |
| A:LYS115 NZ | C:DT16 OP1 | 2.320 | **Suspiciously short** contact—inspect |
| D:LYS115 NZ | B:DT16 OP1 | 2.424 | Short contact—inspect |

**Important quality warning:** A full 3.6-Å heavy-atom search of the supplied PDB found **42 protein–DNA atom pairs shorter than 2.2 Å**, which may indicate severe steric overlaps or unphysical geometry. Do not present these as genuine H-bonds or experimentally demonstrated specific binding. This needs detailed validation, minimization/refinement and ideally experimental study. Earlier figure labels such as **1.469 Å** have not been reproduced for the listed LYS115–OP1 atom pair and should be checked before being quoted in a paper/poster.

Review `results/id143_contact_audit.txt`, [`docs/STRUCTURE_ANALYSIS.md`](docs/STRUCTURE_ANALYSIS.md), and [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md).

## Repository documentation

- **Setup and environments:** [`docs/INSTALLATION.md`](docs/INSTALLATION.md)
- **From reference to candidate:** [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md)
- **How to inspect structures and validate contacts:** [`docs/STRUCTURE_ANALYSIS.md`](docs/STRUCTURE_ANALYSIS.md)
- **Validation, interpretation, and scientific limits:** [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md)
- **Upload using GitHub web or terminal:** [`docs/UPLOAD_TO_GITHUB.md`](docs/UPLOAD_TO_GITHUB.md)

## Citation and credit

Study topic: **AI-Driven De Novo Design of DNA-Binding Proteins**. Project author (as listed in study poster): **Yip Kheng Yeong**, Department of Bioscience and Biotechnology, National Taiwan Ocean University. Advisor: **Prof. Wen-Hsiung Tsou**.

Please cite original work on [3KMD](https://www.rcsb.org/structure/3KMD), [RFdiffusion](https://github.com/RosettaCommons/RFdiffusion), [LigandMPNN](https://github.com/dauparas/LigandMPNN), [Boltz](https://github.com/jwohlwend/boltz), and [ChimeraX](https://www.rbvi.ucsf.edu/chimerax/) as appropriate. The bundled configurations and scripts document a research workflow; external model weights or code are not redistributed.

**License:** No open-source license has been selected by the project author. Contact the author before reusing project-authored materials; check individual software/data licenses separately.
