# github-repo-updater

[![License](https://img.shields.io/badge/license-MIT-informational)](#license)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![OS](https://img.shields.io/badge/OS-Windows%20%7C%20Linux-blue)

**ZIP-based updater from GitHub to a local folder with SHA tracking and robust cleanup.**

This script downloads a repository branch as a ZIP, safely extracts it, and overwrites an existing local folder. It records the latest commit SHA in `.last_sha` to skip redundant updates and includes lock-safe cleanup for Windows.

## Features
- Download a repo branch as ZIP and **safe-extract** (zip-slip guarded).
- **Overwrite** the target folder while preserving structure.
- Track remote version with a `.last_sha` file (skip if up-to-date).
- Robust cleanup on Windows (handles read-only/temporarily locked files).
- Clear exit codes for scripting/CI.

## Requirements
- Python 3.9+
- Packages: `requests`, `python-dotenv`

```bash
pip install -r requirements.txt
# or
pip install requests python-dotenv
```

## Authentication

Set a GitHub **Personal Access Token** in the environment (preferred):

```bash
# Windows (PowerShell)
setx GITHUB_TOKEN "ghp_xxx"

# macOS/Linux (bash)
export GITHUB_TOKEN="ghp_xxx"
```

For public repos, the `public_repo` scope is sufficient; for private repos, use `repo`.

> If your local copy of the script also supports reading from a `.env` file, that’s optional—environment variables are recommended.

## Usage

Place `UpdateFromGitHub.py` in the repo root, then run:

```bash
# Windows (PowerShell)
python .\UpdateFromGitHub.py --user <github_user> --repo <repo_name> --output <local_folder> [--branch main]

# macOS / Linux
python3 ./UpdateFromGitHub.py --user <github_user> --repo <repo_name> --output <local_folder> [--branch main]
```

### Example

```bash
python UpdateFromGitHub.py --user yourname --repo some-repo --output D:\Workspace\some-repo --branch main
```

## Arguments

* `--user`  GitHub username
* `--repo`  Repository name
* `--output`  Target folder to overwrite with extracted files
* `--branch` *(optional)* Branch name; defaults to the repo’s default branch

## Exit codes

* `0` success (including “already up to date”)
* `1` failure (network/ZIP/extract/cleanup errors, etc.)

## Notes

* `.last_sha` is written to the **target** (`--output`) directory.
* Antivirus/indexers may briefly lock files; the script retries and clears read-only flags automatically.
* Use in CI or scheduled tasks to keep a local mirror current.

## License

[MIT](LICENSE)

