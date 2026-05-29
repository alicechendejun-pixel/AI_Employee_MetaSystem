import time
import requests
import subprocess
import sys

CLIENT_ID = "178c6fc778ccc68e1d6a"
print("Requesting new device code...")
res = requests.post(
    "https://github.com/login/device/code",
    data={"client_id": CLIENT_ID, "scope": "repo"},
    headers={"Accept": "application/json"}
)
data = res.json()

with open(r"G:\我的云端硬盘\09-AI员工系统\device_code.txt", "w", encoding="utf-8") as f:
    f.write(data["user_code"])

print("Polling for user authorization...")
token = None
for _ in range(120): # 10 minutes timeout
    res_token = requests.post(
        "https://github.com/login/oauth/access_token",
        data={"client_id": CLIENT_ID, "device_code": data["device_code"], "grant_type": "urn:ietf:params:oauth:grant-type:device_code"},
        headers={"Accept": "application/json"}
    )
    token_data = res_token.json()
    if "access_token" in token_data:
        token = token_data["access_token"]
        print("Token acquired!")
        break
    time.sleep(5)

if token:
    print("Pushing to GitHub...")
    repo_url = f"https://oauth2:{token}@github.com/alicechendejun-pixel/AI_Employee_MetaSystem.git"
    CWD = r"G:\我的云端硬盘\09-AI员工系统"
    subprocess.run(["git", "remote", "remove", "origin"], cwd=CWD, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "remote", "add", "origin", repo_url], cwd=CWD)
    push_res = subprocess.run(["git", "push", "-u", "origin", "master"], cwd=CWD)
    if push_res.returncode == 0:
        print("PUSH SUCCESSFUL!")
    else:
        print("PUSH FAILED.")
else:
    print("Authorization timed out.")
