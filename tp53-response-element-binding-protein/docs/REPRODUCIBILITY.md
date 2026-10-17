# Pipeline and provenance

## 1. Reference structure

`inputs/3KMD.pdb` is an **original 3KMD experimental reference**; it is *not* designed id143. In reference model protein chains A–D and DNA strands E/F are present. Inspect before use.

## 2. t9 scaffold RFD3

`inputs/rfd3_na_test9.json` constrains DNA E1–19 / F1–19 and TP53 chain A motif ranges A118–124, A241–248, A273–285. Run `bash scripts/run_rfd3.sh` with an installed compatible RFD3 checkpoint. The selected historical RFD3 backbone was documented as `rfd3_na_test9_dsDNA_3KMD_fullDNA_fixed_A118_124_two_p53_motifs_6_model_3.cif`, but this original intermediate file was **not uploaded**.

## 3. LigandMPNN

After RFD3: first check polymer chain IDs, then design chain C (if that matches selected CIF). Run `bash scripts/run_ligandmpnn.sh /absolute/path/to/backbone.cif`. Original t9 LigandMPNN outputs included 100 candidates, later lower-temperature t9-converge runs and an id143 designation; the complete intermediate FASTA and exact selection/seed history are **not available** in this release.

## 4. Recreate input for independent Boltz prediction

`boltz_input/id143_homodimer.yaml` is built directly from `results/structures/id143_design_complex.pdb`; it contains two identical 123-residue protein chains A/D and two DNA strands B/C, each `GGGCATGCCTAGGCATGCCC` (5′→3′). This 20-nt Boltz construct differs from the original 3KMD 19-nt RFD3 reference segments. It enables **a new prediction of the same molecular composition**, but does not prove historical output reproducibility. The original Boltz confidence JSON is missing; metric values are transcribed into `results/id143_reported_boltz_metrics.tsv` and labeled accordingly.

Run `bash scripts/run_boltz.sh boltz_input/id143_homodimer.yaml` after installing Boltz. Use `BOLTZ_SEED=1` for an explicit seed. Review `--use_msa_server` privacy implications in the script.

## 5. Independently inspect supplied design (recommended)

```bash
python scripts/inspect_structure.py results/structures/id143_design_complex.pdb
python scripts/analyze_contacts.py results/structures/id143_design_complex.pdb \
  --cutoff 3.6 --output results/id143_contacts_recomputed.tsv
```

For scientific reporting, include contact atom names, chain IDs, measured distances, quality flags and analysis cutoff. An atom-pair distance by itself is **not** enough to call a hydrogen bond.

## 6. Limitations of this source set

Available: final id143 PDB + extracted protein/DNA sequences + reference 3KMD + documented t9 config and utilities. Missing: original RFD3 intermediate, full LigandMPNN candidate FASTA, full Boltz run artifacts/checkpoints, input provenance/seed/version locks, experimental DNA binding assay. Accordingly, this repository supports model inspection and partial method repetition, not exact bitwise recreation of the historical design selection.
