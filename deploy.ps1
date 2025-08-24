Write-Host "====================================" -ForegroundColor Cyan
Write-Host "失眠中医智能诊疗系统 - 一键部署" -ForegroundColor Cyan  
Write-Host "====================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "第1步：检查Git安装..." -ForegroundColor Yellow
try {
    git --version | Out-Null
    Write-Host "✅ Git已安装" -ForegroundColor Green
} catch {
    Write-Host "❌ Git未安装，请先安装Git: https://git-scm.com/download/windows" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

Write-Host ""
Write-Host "第2步：初始化Git仓库..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    git init
    Write-Host "✅ Git仓库已初始化" -ForegroundColor Green
} else {
    Write-Host "✅ Git仓库已存在" -ForegroundColor Green
}

Write-Host ""
Write-Host "第3步：配置Git用户..." -ForegroundColor Yellow
git config --global user.email "doctor@tcm.com" 2>$null
git config --global user.name "TCM Doctor" 2>$null
Write-Host "✅ Git配置完成" -ForegroundColor Green

Write-Host ""
Write-Host "第4步：添加文件到Git..." -ForegroundColor Yellow
git add .
Write-Host "✅ 文件已添加" -ForegroundColor Green

Write-Host ""
Write-Host "第5步：提交代码..." -ForegroundColor Yellow
git commit -m "失眠中医智能诊疗系统 - 初始版本"
Write-Host "✅ 代码已提交" -ForegroundColor Green

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "✅ 本地Git准备完成！" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 接下来需要你手动完成：" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. 访问 https://github.com" -ForegroundColor White
Write-Host "2. 登录/注册账号" -ForegroundColor White
Write-Host "3. 创建新仓库：insomnia-ai-doctor" -ForegroundColor White
Write-Host "4. 复制仓库地址" -ForegroundColor White
Write-Host ""
Write-Host "5. 在此窗口输入以下命令：" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/你的用户名/insomnia-ai-doctor.git" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "6. 访问 https://vercel.com" -ForegroundColor White
Write-Host "7. 用GitHub登录" -ForegroundColor White
Write-Host "8. 导入项目，Root Directory设为 'frontend'" -ForegroundColor White
Write-Host "9. 点击Deploy" -ForegroundColor White
Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan

Read-Host "按回车键退出"