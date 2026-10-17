#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGE="${RFD3_IMAGE:-rosettacommons/foundry}"
CHECKPOINT="${RFD3_CHECKPOINT:-$ROOT/weights/rfd3_latest.ckpt}"
[[ -f "$ROOT/inputs/3KMD.pdb" ]] || { echo 'Missing inputs/3KMD.pdb' >&2; exit 2; }
[[ -f "$CHECKPOINT" ]] || { echo "Missing RFD3 checkpoint: $CHECKPOINT" >&2; exit 2; }
command -v docker >/dev/null || { echo 'Docker not found' >&2; exit 2; }
# The checkpoint must be within the repository's mounted weights/ directory.
[[ "$CHECKPOINT" == "$ROOT/weights/rfd3_latest.ckpt" ]] || {
  echo 'Copy your checkpoint into weights/rfd3_latest.ckpt; other host paths are not mounted.' >&2; exit 2;
}
mkdir -p "$ROOT/outputs/rfd3/t9"
docker run --gpus all --rm \
  -v "$ROOT:/work" -w /work "$IMAGE" rfd3 \
  out_dir=outputs/rfd3/t9 \
  inputs=inputs/rfd3_na_test9.json \
  ckpt_path=/work/weights/rfd3_latest.ckpt \
  inference_engine=rfdiffusion3 \
  diffusion_batch_size=4 n_batches=25
