# GitHub Repo Updater

A lightweight Python script that auto-updates a local folder from any GitHub repository by downloading the latest zip and extracting its contents directly into a target directory.

## 📦 Features

- ✅ Supports both public and private GitHub repos
- ✅ Avoids unnecessary downloads using commit SHA comparison
- ✅ Auto-detects default branch if not specified
- ✅ Overwrites existing files in the target folder
- ✅ Loads GitHub token securely from `.env`

## ⚙️ Requirements

- Python 3.7+
- `requests`
- `python-dotenv`

Install dependencies:


pip install -r requirements.txt

## 🚀 Usage
```
python UpdateFromGitHub.py --user <github_user> --repo <repo_name> --output <target_folder> [--branch <branch_name>]
```
## Examples
Update the latest version of a repo into a local folder:
```
python UpdateFromGitHub.py --user octocat --repo Hello-World --output D:\Projects\Hello
```

Using a specific branch:
```
python UpdateFromGitHub.py --user octocat --repo Hello-World --branch dev --output D:\Projects\Hello
```

## 🔐 Authentication

This script requires a GitHub Personal Access Token (PAT) stored in a `.env` file:

```
GITHUB_TOKEN=ghp_your_actual_token
```

Save the file as:
```
../AccountSecrets/config_github.env
```
(relative to the script location)

A sample file is included as .env.example in the project root.
Rename it and provide your own token as needed.

📁 Folder structure:

```text
your_project/
├── UpdateFromGitHub.py
├── .env.example          # Sample config
└── ../AccountSecrets/
    └── config_github.env # Actual token used by the script
```

## 📄 .gitignore (recommended)
```
repo.zip
__temp_extract__/
*.env
.vscode/
.idea/
```

## 📄 License
MIT License


