import os
import requests
import zipfile
import argparse
import shutil
from dotenv import load_dotenv

# --- Parse command-line arguments ---
parser = argparse.ArgumentParser(description="Download and update GitHub repo to a local folder (with overwrite)")
parser.add_argument("--user", required=True, help="GitHub username")
parser.add_argument("--repo", required=True, help="Repository name")
parser.add_argument("--branch", help="Branch name (optional, will use default branch if not specified)")
parser.add_argument("--output", required=True, help="Target folder to extract and overwrite files into")
args = parser.parse_args()

# --- Load GITHUB_TOKEN from .env ---
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'AccountSecrets', 'config_github.env'))
load_dotenv(env_path)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    print("❌ Failed to load GITHUB_TOKEN from .env")
    exit(1)

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

USER = args.user
REPO = args.repo
OUTPUT_FOLDER = args.output

# --- Determine branch (if not provided) ---
if args.branch:
    BRANCH = args.branch
else:
    print("🔍 No branch specified. Fetching default branch from GitHub...")
    repo_api_url = f"https://api.github.com/repos/{USER}/{REPO}"
    try:
        repo_info = requests.get(repo_api_url, headers=HEADERS, timeout=10).json()
        BRANCH = repo_info["default_branch"]
        print(f"📌 Default branch: {BRANCH}")
    except Exception as e:
        print(f"❌ Failed to get default branch: {e}")
        exit(1)

ZIP_URL = f"https://github.com/{USER}/{REPO}/archive/refs/heads/{BRANCH}.zip"
API_URL = f"https://api.github.com/repos/{USER}/{REPO}/branches/{BRANCH}"
SHA_FILE = os.path.join(OUTPUT_FOLDER, ".last_sha")

# --- Check latest SHA on GitHub ---
print("🔍 Checking latest commit SHA from GitHub...")
try:
    resp = requests.get(API_URL, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    latest_sha = resp.json()["commit"]["sha"]
    print(f"🔧 Latest commit SHA: {latest_sha}")
except Exception as e:
    print(f"❌ Failed to fetch SHA: {e}")
    exit(1)

# --- Compare local SHA ---
if os.path.exists(SHA_FILE):
    with open(SHA_FILE, "r") as f:
        local_sha = f.read().strip()
else:
    local_sha = ""

if latest_sha == local_sha:
    print("✅ Already up to date. No download needed.")
    exit(0)

# --- Download ZIP ---
print("⬇️ New version detected. Downloading ZIP...")
r = requests.get(ZIP_URL, headers=HEADERS, timeout=30)
with open("repo.zip", 'wb') as f:
    f.write(r.content)

# --- Extract ZIP to temp folder ---
print("🧩 Extracting ZIP...")
temp_extract_folder = "__temp_extract__"
if os.path.exists(temp_extract_folder):
    shutil.rmtree(temp_extract_folder)
os.makedirs(temp_extract_folder, exist_ok=True)

with zipfile.ZipFile("repo.zip", 'r') as zip_ref:
    zip_ref.extractall(temp_extract_folder)

# --- Copy files into target folder (overwrite mode) ---
extracted_folder_name = os.path.join(temp_extract_folder, f"{REPO}-{BRANCH}")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

print(f"📂 Copying contents from {extracted_folder_name} to {OUTPUT_FOLDER} (overwrite enabled)...")
for item in os.listdir(extracted_folder_name):
    src = os.path.join(extracted_folder_name, item)
    dst = os.path.join(OUTPUT_FOLDER, item)
    if os.path.isdir(src):
        if not os.path.exists(dst):
            shutil.copytree(src, dst)
        else:
            for root, dirs, files in os.walk(src):
                rel_path = os.path.relpath(root, src)
                target_dir = os.path.join(dst, rel_path)
                os.makedirs(target_dir, exist_ok=True)
                for file in files:
                    shutil.copy2(os.path.join(root, file), os.path.join(target_dir, file))
    else:
        shutil.copy2(src, dst)

# --- Cleanup ---
shutil.rmtree(temp_extract_folder)
if os.path.exists("repo.zip"):
    os.remove("repo.zip")
    print("🗑️ Removed downloaded repo.zip")

# --- Save latest SHA
with open(SHA_FILE, "w") as f:
    f.write(latest_sha)

print("🎉 Update completed successfully.")
