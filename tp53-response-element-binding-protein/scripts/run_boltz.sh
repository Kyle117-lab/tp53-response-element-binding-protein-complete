#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INPUT="${1:-$ROOT/boltz_input/id143_homodimer.yaml}"
[[ -f "$INPUT" ]] || { echo "Missing Boltz YAML: $INPUT. See sequences/README.md" >&2; exit 2; }
command -v boltz >/dev/null || { echo 'Activate Boltz conda environment first' >&2; exit 2; }
mkdir -p "$ROOT/outputs/boltz"
args=("$INPUT" --out_dir "$ROOT/outputs/boltz/id143" --override)
if [[ "${BOLTZ_USE_MSA_SERVER:-1}" == "1" ]]; then
  echo 'Notice: --use_msa_server sends sequence information to an external service.'
  args+=(--use_msa_server)
else
  echo 'MSA server disabled: provide an MSA in your YAML or set msa: empty (lower accuracy).'
fi
if [[ -n "${BOLTZ_SEED:-}" ]]; then args+=(--seed "$BOLTZ_SEED"); fi
boltz predict "${args[@]}"
