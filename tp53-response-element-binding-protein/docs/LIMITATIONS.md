# Limitations and responsible interpretation

**Predicted ≠ measured.** This is a computational structural design. Protein–DNA binding affinity, specific TP53 response-element recognition, in-cell TP53-related function, and oligomeric state have not been validated experimentally.

**Model quality issue:** the uploaded id143 coordinate file exhibits 42 protein–DNA nonbonded heavy-atom pairs shorter than 2.2 Å when scanned with a 3.6 Å cutoff (see CSV/TSV and audit). These may indicate coordinate clashes/unphysical interface packing; investigate side-chain geometry, DNA geometry and any structural conversion artifacts before drawing strong conclusions.

**Reported Boltz scores** in `results/id143_reported_boltz_metrics.tsv` were transcribed from the previous project record, not recalculated from this PDB. Boltz confidence requires saved model-generated confidence JSON.

**Geometric contacts** are not automatically hydrogen bonds. Distances alone cannot establish donor/acceptor identity, protonation, angular geometry, base specificity or biological activity. The 1.469 Å figure annotation does not match the explicit LYS115 NZ–DT16 OP1 atom-pair measurements in the deposited structure (2.320 Å for A/C and 2.424 Å for D/B).

**DNA constructs:** design template in 3KMD/RFD3 uses the original 19-nt strands, whereas selected Boltz homodimer model has two 20-nt palindromic strands. They are not identical molecules; document this distinction when comparing results.

**Next steps:** validate atom names and chain IDs against model software output; model minimization/refinement; clash checks; multi-seed sensitivity; better DNA duplex geometry assessment; optional molecular dynamics and binding free-energy estimates; direct experimental DNA binding and specificity assay.
