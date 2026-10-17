#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LMPNN_DIR="${LMPNN_DIR:-$HOME/DNA_protein_design/LMPNN/LigandMPNN-main}"
BACKBONE="${1:-$ROOT/outputs/rfd3/t9/rfd3_na_test9_dsDNA_3KMD_fullDNA_fixed_A118_124_two_p53_motifs_6_model_3.cif}"
[[ -f "$LMPNN_DIR/run.py" ]] || { echo "Missing LigandMPNN run.py in $LMPNN_DIR" >&2; exit 2; }
[[ -f "$BACKBONE" ]] || { echo "Missing selected t9 RFD3 backbone: $BACKBONE" >&2; exit 2; }
mkdir -p "$ROOT/outputs/ligandmpnn/t9"
echo 'CHECK chain IDs with inspect_structure.py first; t9 RFD3 output used DNA A/B and protein C.'
cd "$LMPNN_DIR"
python run.py \
  --model_type ligand_mpnn \
  --pdb_path "$BACKBONE" \
  --out_folder "$ROOT/outputs/ligandmpnn/t9" \
  --chains_to_design "${PROTEIN_CHAIN:-C}" \
  --number_of_batches "${LMPNN_BATCHES:-100}" --batch_size 1 \
  --temperature "${LMPNN_TEMPERATURE:-0.1}" \
  --pack_side_chains 1 --pack_with_ligand_context 1
