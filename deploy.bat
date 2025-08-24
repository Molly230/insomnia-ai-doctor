@echo off
echo ====================================
echo 失眠中医智能诊疗系统 - 一键部署
echo ====================================

echo.
echo 第1步：检查Git安装...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git未安装，请先安装Git: https://git-scm.com/download/windows
    pause
    exit /b 1
)
echo ✅ Git已安装

echo.
echo 第2步：初始化Git仓库...
if not exist .git (
    git init
    echo ✅ Git仓库已初始化
) else (
    echo ✅ Git仓库已存在
)

echo.
echo 第3步：添加文件到Git...
git add .
git config --global user.email "doctor@tcm.com" 2>nul
git config --global user.name "TCM Doctor" 2>nul

echo.
echo 第4步：提交代码...
git commit -m "失眠中医智能诊疗系统 - 初始版本"

echo.
echo ====================================
echo ✅ 本地Git准备完成！
echo ====================================
echo.
echo 📋 接下来需要你手动完成：
echo.
echo 1. 访问 https://github.com
echo 2. 登录/注册账号
echo 3. 创建新仓库：insomnia-ai-doctor
echo 4. 复制仓库地址
echo.
echo 5. 在此窗口输入以下命令：
echo    git remote add origin https://github.com/你的用户名/insomnia-ai-doctor.git
echo    git push -u origin main
echo.
echo 6. 访问 https://vercel.com
echo 7. 用GitHub登录
echo 8. 导入项目，Root Directory设为 "frontend"
echo 9. 点击Deploy
echo.
echo ====================================
pause