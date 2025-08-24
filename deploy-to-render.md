# 部署到 Render 指南

## 🚀 快速部署步骤

### 1. 推送代码到 GitHub
```bash
git add .
git commit -m "配置Render部署环境"
git push origin main
```

### 2. 在 Render 创建服务

1. 访问 [render.com](https://render.com) 注册账号
2. 点击 "New +" → "Web Service"
3. 连接你的 GitHub 仓库: `insomnia_ai_doctor`
4. 配置服务：

**基本设置:**
- **Name**: `insomnia-ai-doctor`
- **Runtime**: `Python 3`
- **Build Command**: `cd backend && pip install -r requirements.txt`
- **Start Command**: `cd backend && python run.py`

**环境变量:**
```
FLASK_ENV=production
PORT=10000
PYTHONPATH=/opt/render/project/src/backend
```

### 3. 部署
点击 "Create Web Service"，Render 会自动构建和部署。

### 4. 获取你的网站地址
部署完成后，你会得到类似这样的地址：
`https://insomnia-ai-doctor-xxxx.onrender.com`

## 💡 重要提示

- **免费版限制**: 750小时/月，长时间不访问会休眠
- **首次启动**: 可能需要30秒-1分钟启动时间
- **自动部署**: 每次推送到GitHub会自动重新部署

## 🔧 故障排除

如果部署失败，检查日志中的错误信息：
1. Python版本兼容性
2. 依赖包安装问题  
3. 端口配置问题

---

**准备好了？执行第1步推送代码！**