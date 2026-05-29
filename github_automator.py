import time
import requests
import os
import subprocess
import sys

CLIENT_ID = "178c6fc778ccc68e1d6a"
DEVICE_CODE = "5e4b355bd334c15db9cd524dc21d67a75ec935ad"
REPO_NAME = "AI_Employee_MetaSystem"
CWD = r"G:\我的云端硬盘\09-AI员工系统"

print("Waiting for CEO to authorize via GitHub Device URL...")
token = None
for _ in range(120): # Poll for 10 minutes max
    res = requests.post(
        "https://github.com/login/oauth/access_token",
        data={"client_id": CLIENT_ID, "device_code": DEVICE_CODE, "grant_type": "urn:ietf:params:oauth:grant-type:device_code"},
        headers={"Accept": "application/json"}
    )
    data = res.json()
    if "access_token" in data:
        token = data["access_token"]
        print("\n[OK] Authorization successful! Token acquired.")
        break
    if data.get("error") == "authorization_pending":
        print(".", end="", flush=True)
    else:
        print("\n[Error]", data)
        sys.exit(1)
    time.sleep(5)

if not token:
    print("\n[Error] Timeout waiting for authorization.")
    sys.exit(1)

print("\n[1/2] Creating GitHub repository via API...")
res = requests.post(
    "https://api.github.com/user/repos",
    headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json"},
    json={"name": REPO_NAME, "private": False, "description": "CEO's local AI Employee Meta-System registry", "auto_init": False}
)

if res.status_code in (201, 422):
    print("[OK] Repository created or already exists.")
    username = "alicechendejun"
    repo_url = f"https://oauth2:{token}@github.com/{username}/{REPO_NAME}.git"
    
    print("[2/2] Pushing local Git repository to GitHub...")
    subprocess.run(["git", "remote", "remove", "origin"], cwd=CWD, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "remote", "add", "origin", repo_url], cwd=CWD)
    push_res = subprocess.run(["git", "push", "-u", "origin", "master"], cwd=CWD)
    
    if push_res.returncode == 0:
        print("\n🎉 MISSION ACCOMPLISHED! ALL CODE PUSHED SUCCESSFULLY!")
    else:
        print("\n[Error] Git push failed.")
else:
    print(f"\n[Error] Failed to create repo. Status: {res.status_code}, Body: {res.text}")
