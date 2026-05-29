@echo off
chcp 65001 >nul
title AI Employee Meta-System 自动推送器
echo ===================================================
echo 👑 正在将您的 20 个兵器库和系统内核推送到云端...
echo ===================================================
echo.
cd /d "G:\我的云端硬盘\09-AI员工系统"

git remote remove origin 2>nul
git remote add origin https://github.com/alicechendejun-pixel/AI_Employee_MetaSystem.git

echo 正在执行极速推送...
git push -u origin master

echo.
echo ===================================================
echo ✅ 推送已完成！您的 GitHub 仓库已全套就绪。
echo ===================================================
pause
