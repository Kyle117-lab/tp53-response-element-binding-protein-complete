# Publish to GitHub

## Recommended: upload ZIP contents using GitHub web

1. Create a new GitHub repository named `tp53-response-element-binding-protein` (choose public/private after checking lab/advisor policy).
2. Extract the supplied `.zip` file on your computer.
3. In the empty repository, choose **Add file → Upload files** and drag the **files inside** the unzipped directory into GitHub. Preserve the directories; if the web upload does not preserve a directory structure on your platform, use the command line method below.
4. Commit with message `Add 3KMD DNA-binding protein project and verified id143 model`.
5. On GitHub, check that `README.md`, `results/structures/id143_design_complex.pdb`, `sequences/`, `scripts/`, `docs/` and `figures/` display correctly.

## Command line (recommended for preserving folders)

Run from the repository root after extracting:

```bash
git init
git add .
git commit -m "Initial TP53 DNA-binding protein project with id143 structure"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/tp53-response-element-binding-protein.git
git push -u origin main
```

Create the empty repository on GitHub first, and replace `YOUR-USERNAME`. Authenticate with GitHub CLI (`gh auth login`) or a supported credential manager; GitHub does not support account passwords for Git over HTTPS.

## Before switching to Public

Confirm laboratory consent, research ownership, rights to use institutional emblems/posters, and third-party assets. No model checkpoints, credentials, or other people's unpublished data are included. No automatic open-source license is granted by omitting a LICENSE file. If your instructor wants a license, obtain approval and add one separately.
