# Installation / Environment setup

## Minimal (no GPU; inspect deposited output)

Ubuntu Linux, Python 3.10+ recommended:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-analysis.txt
python scripts/check_repository.py
python scripts/inspect_structure.py results/structures/id143_design_complex.pdb
```

The analysis scripts use **Biopython** and **PyYAML** only. They do **not** require running RFD3, LigandMPNN or Boltz.

## Full design (requires NVIDIA GPU and sufficient storage)

- Ubuntu + NVIDIA drivers/CUDA compatible with the chosen software stack, confirm `nvidia-smi`.
- Docker with NVIDIA Container Toolkit, confirm `docker run --rm --gpus all ...` works.
- Foundry/RFD3 Docker image + authorized matching checkpoint (`weights/rfd3_latest.ckpt`), installed separately.
- LigandMPNN installation with model weights, activate the `pmpnn` Conda environment and configure `LMPNN_DIR` if necessary.
- Boltz installation with model weights, activate the `boltz` Conda environment.
- UCSF ChimeraX for GUI rendering (installed separately).

Project history used e.g. `rosettacommons/foundry` for RFD3, `~/DNA_protein_design/LMPNN/LigandMPNN-main` for LigandMPNN and `~/DNA_protein_design/boltz-main` for Boltz. These are example paths, not installation prerequisites for the CPU-only analysis.

Check software versions:

```bash
nvidia-smi
docker --version
conda --version
python --version
python -c 'import Bio, yaml; print(Bio.__version__, yaml.__version__)'
boltz predict --help
```

For installation, follow the official repositories: [LigandMPNN](https://github.com/dauparas/LigandMPNN), [Boltz](https://github.com/jwohlwend/boltz) and the RFD3 provider's current documentation. Keep local version/seed/checkpoint records for reproducibility.
