# 微信公众号配置指南

## 1. 环境配置

### 复制配置文件
```bash
cp .env.example .env
```

### 编辑 .env 文件
```bash
# 微信公众号配置
WECHAT_APP_ID=你的微信公众号AppID
WECHAT_APP_SECRET=你的微信公众号AppSecret  
WECHAT_TOKEN=你设置的Token（建议用随机字符串）
WECHAT_ENCODING_AES_KEY=消息加解密密钥（可选）

# Redis配置（用于存储用户会话）
REDIS_URL=redis://localhost:6379/0
```

## 2. 微信公众平台配置

### 登录微信公众平台
1. 访问 https://mp.weixin.qq.com
2. 用你的微信公众号登录

### 基本配置
1. 左侧菜单：开发 → 基本配置
2. 获取 AppID 和 AppSecret
3. 设置服务器配置：
   - URL: `https://你的域名/api/wechat`
   - Token: 与.env中WECHAT_TOKEN保持一致
   - 消息加解密方式：明文模式（或选择兼容模式）

### 接口权限
1. 左侧菜单：开发 → 接口权限
2. 确保以下权限已开通：
   - 基础支持 → 获取用户基本信息
   - 自定义菜单 → 自定义菜单创建接口
   - 消息管理 → 客服接口

## 3. 部署和启动

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动Redis服务
```bash
# Windows
# 下载并启动Redis

# Linux/Mac
redis-server
```

### 启动应用
```bash
python run.py
```

### 创建菜单
```bash
curl -X POST http://localhost:5000/api/wechat/menu/create
```

## 4. 功能说明

### 主菜单结构
```
开始问诊          中医服务          帮助中心
                ├─ 失眠咨询       ├─ 使用说明  
                ├─ 我的报告       └─ 联系医师
                └─ 中医知识
```

### 对话流程
1. **用户关注** → 欢迎消息
2. **开始问诊** → 19题问诊流程  
3. **智能对话** → 中医咨询问答
4. **查看报告** → 个性化治疗方案

### 会话管理
- 使用Redis存储用户会话状态
- 会话过期时间：1小时
- 支持中途暂停和恢复问诊

## 5. 测试验证

### 本地测试
1. 使用ngrok等工具映射本地端口
2. 设置微信服务器URL为ngrok地址
3. 关注测试号进行功能测试

### 生产部署
1. 购买服务器和域名
2. 配置HTTPS证书
3. 更新微信服务器配置
4. 部署代码并启动服务

## 6. 常见问题

### Q: 微信验证失败？
A: 检查Token是否一致，URL是否正确访问

### Q: 菜单不显示？  
A: 确认接口权限，尝试重新创建菜单

### Q: Redis连接失败？
A: 检查Redis服务是否启动，连接配置是否正确

### Q: 会话丢失？
A: 检查Redis配置，确认会话过期时间设置

## 7. 扩展功能

- [ ] 集成AI大模型进行智能对话
- [ ] 添加语音消息处理  
- [ ] 支持图片上传（舌诊等）
- [ ] 模板消息推送提醒
- [ ] 微信支付集成

---

💡 **提示**: 确保服务器有公网IP和域名，微信要求必须使用HTTPS